import React, { useState, useMemo } from 'react';
import {
  Page,
  Masthead,
  MastheadMain,
  MastheadBrand,
  MastheadLogo,
  PageSection,
  Card,
  CardTitle,
  CardBody,
  Form,
  FormGroup,
  TextInput,
  FormSelect,
  FormSelectOption,
  Button,
  Alert,
  Spinner,
  DescriptionList,
  DescriptionListGroup,
  DescriptionListTerm,
  DescriptionListDescription,
  Badge,
  Content,
  Divider,
} from '@patternfly/react-core';
import GlobeIcon from '@patternfly/react-icons/dist/esm/icons/globe-icon';
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from 'recharts';
import GlobePanel from './GlobePanel';
import coordData from './cityCoords.json';
import './App.css';

const CONTINENTS = [
  'Africa',
  'Antarctica',
  'Asia',
  'Europe',
  'North America',
  'Oceania',
  'South America',
];

const CHART_COLOURS = [
  '#0066cc', '#4cb140', '#f0ab00', '#c9190b',
  '#6753ac', '#009596', '#ec7a08', '#8a8d90',
  '#1f77b4', '#2ca02c',
];

function App() {
  const [queryType, setQueryType] = useState('city');
  const [queryInput, setQueryInput] = useState('');
  const [continentInput, setContinentInput] = useState(CONTINENTS[0]);
  const [result, setResult] = useState(null);
  const [countryDetail, setCountryDetail] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [globeTarget, setGlobeTarget] = useState({ lat: null, lng: null, label: null });

  const lookupCoords = (cityName, countryCode) => {
    const cityKey = `${cityName}|${countryCode}`;
    if (coordData.cities[cityKey]) {
      const [lat, lng] = coordData.cities[cityKey];
      return { lat, lng };
    }
    if (coordData.countries[countryCode]) {
      const [lat, lng] = coordData.countries[countryCode];
      return { lat, lng };
    }
    return null;
  };

  const clearResults = () => {
    setResult(null);
    setCountryDetail(null);
    setError(null);
  };

  const fetchCountryForCity = async (countryCode) => {
    try {
      const response = await fetch(`/api/country/detail?code=${encodeURIComponent(countryCode)}`);
      const data = await response.json();
      if (response.ok && data.country) {
        setCountryDetail(data);
      }
    } catch {
      // silently fail — the city result is still shown
    }
  };

  const fetchCountryDetail = async (countryName, countryCode) => {
    setLoading(true);
    clearResults();
    setQueryType('country');
    if (countryName) setQueryInput(countryName);

    const param = countryCode
      ? `code=${encodeURIComponent(countryCode)}`
      : `name=${encodeURIComponent(countryName)}`;

    try {
      const response = await fetch(`/api/country/detail?${param}`);
      const data = await response.json();

      if (response.ok && data.country) {
        setCountryDetail(data);
        if (data.country.Name) setQueryInput(data.country.Name);
        if (data.capital) {
          const pos = lookupCoords(data.capital.Name, data.country.Code);
          if (pos) setGlobeTarget({ ...pos, label: data.capital.Name });
        } else {
          const fallback = coordData.countries[data.country.Code];
          if (fallback) setGlobeTarget({ lat: fallback[0], lng: fallback[1], label: data.country.Name });
        }
      } else if (response.ok) {
        setError('Country not found.');
      } else {
        setError(data.message || 'Unknown error from API.');
      }
    } catch {
      setError('Could not fetch data. Is the API available?');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (queryType === 'continent') {
      setLoading(true);
      clearResults();

      try {
        const response = await fetch(`/api/continent?name=${encodeURIComponent(continentInput)}`);
        const data = await response.json();

        if (response.ok) {
          setResult(data);
          const center = coordData.continents[continentInput];
          if (center) setGlobeTarget({ lat: center[0], lng: center[1], label: continentInput });
        } else {
          setError(data.message || 'Unknown error from API.');
        }
      } catch {
        setError('Could not fetch data. Is the API available?');
      } finally {
        setLoading(false);
      }
      return;
    }

    const trimmed = queryInput.trim();
    if (!trimmed) {
      setError('Please enter a name to query.');
      clearResults();
      return;
    }

    setLoading(true);
    clearResults();

    if (queryType === 'country') {
      await fetchCountryDetail(trimmed);
      return;
    }

    const url = `/api/city?name=${encodeURIComponent(trimmed)}`;

    try {
      const response = await fetch(url);
      const data = await response.json();

      if (response.ok) {
        setResult(data);
        if (data.length >= 1) {
          const city = data[0];
          const pos = lookupCoords(city.Name, city.CountryCode);
          if (pos) setGlobeTarget({ ...pos, label: city.Name });
        }
        if (data.length === 1) {
          fetchCountryForCity(data[0].CountryCode);
        }
      } else {
        setError(data.message || 'Unknown error from API.');
      }
    } catch {
      setError('Could not fetch data. Is the API available?');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleSubmit();
    }
  };

  const handleQueryTypeChange = (_event, value) => {
    setQueryType(value);
    clearResults();
  };

  const renderCityCard = (item, index, total) => (
    <Card key={item.ID || index}>
      <CardTitle>
        {total > 1 ? `Result ${index + 1} of ${total}` : 'City'}
      </CardTitle>
      <CardBody>
        <DescriptionList isHorizontal>
          <DescriptionListGroup>
            <DescriptionListTerm>Name</DescriptionListTerm>
            <DescriptionListDescription>{item.Name}</DescriptionListDescription>
          </DescriptionListGroup>
          <DescriptionListGroup>
            <DescriptionListTerm>Country</DescriptionListTerm>
            <DescriptionListDescription>
              <Badge isRead>{item.CountryCode}</Badge>
            </DescriptionListDescription>
          </DescriptionListGroup>
          <DescriptionListGroup>
            <DescriptionListTerm>District</DescriptionListTerm>
            <DescriptionListDescription>{item.District}</DescriptionListDescription>
          </DescriptionListGroup>
          <DescriptionListGroup>
            <DescriptionListTerm>Population</DescriptionListTerm>
            <DescriptionListDescription>
              {item.Population?.toLocaleString()}
            </DescriptionListDescription>
          </DescriptionListGroup>
        </DescriptionList>
        {total > 1 && (
          <div className="world-sub-section">
            <Button
              variant="link"
              isInline
              onClick={() => fetchCountryDetail(null, item.CountryCode)}
            >
              View country details
            </Button>
          </div>
        )}
      </CardBody>
    </Card>
  );

  const preparePieData = (languages) => {
    if (!languages || !languages.length) return [];

    const significant = [];
    let otherTotal = 0;

    for (const lang of languages) {
      const pct = parseFloat(lang.Percentage);
      if (pct >= 2) {
        significant.push({
          name: lang.Language,
          value: pct,
          official: lang.IsOfficial === 'T',
        });
      } else {
        otherTotal += pct;
      }
    }

    if (otherTotal > 0) {
      significant.push({ name: 'Other', value: parseFloat(otherTotal.toFixed(1)), official: false });
    }

    return significant;
  };

  const renderLanguagesPie = (languages) => {
    const data = preparePieData(languages);
    if (!data.length) return null;

    return (
      <div className="world-sub-section">
        <Content><strong>Languages</strong></Content>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={80}
              label={({ name, value }) => `${name} ${value}%`}
            >
              {data.map((entry, i) => (
                <Cell key={entry.name} fill={CHART_COLOURS[i % CHART_COLOURS.length]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value, name, props) => {
                const suffix = props.payload.official ? ' (Official)' : '';
                return [`${value}%${suffix}`, name];
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderCitiesBar = (cities, capitalId) => {
    if (!cities || !cities.length) return null;

    const data = cities.map((city) => ({
      name: city.Name,
      population: city.Population,
      isCapital: city.ID === capitalId,
    }));

    return (
      <div className="world-sub-section">
        <Content><strong>Top Cities</strong></Content>
        <ResponsiveContainer width="100%" height={Math.max(250, data.length * 32)}>
          <BarChart data={data} layout="vertical" margin={{ left: 20, right: 20 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis
              type="number"
              tickFormatter={(v) => v >= 1000000 ? `${(v / 1000000).toFixed(1)}M` : `${(v / 1000).toFixed(0)}K`}
            />
            <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 12 }} />
            <Tooltip formatter={(value) => [value.toLocaleString(), 'Population']} />
            <Bar dataKey="population">
              {data.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={entry.isCapital ? '#c9190b' : '#0066cc'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <div className="world-chart-legend">
          <span className="world-legend-dot world-legend-capital" /> Capital
          <span className="world-legend-dot world-legend-city" /> City
        </div>
      </div>
    );
  };

  const renderCountryCard = () => {
    if (!countryDetail) return null;

    const { country, languages, cities, capital } = countryDetail;

    return (
      <Card>
        <CardTitle>
          {country.Name} <Badge isRead>{country.Code}</Badge>
        </CardTitle>
        <CardBody>
          <DescriptionList isHorizontal>
            <DescriptionListGroup>
              <DescriptionListTerm>Continent</DescriptionListTerm>
              <DescriptionListDescription>{country.Continent}</DescriptionListDescription>
            </DescriptionListGroup>
            <DescriptionListGroup>
              <DescriptionListTerm>Region</DescriptionListTerm>
              <DescriptionListDescription>{country.Region}</DescriptionListDescription>
            </DescriptionListGroup>
            <DescriptionListGroup>
              <DescriptionListTerm>Population</DescriptionListTerm>
              <DescriptionListDescription>
                {country.Population?.toLocaleString()}
              </DescriptionListDescription>
            </DescriptionListGroup>
            <DescriptionListGroup>
              <DescriptionListTerm>Surface Area</DescriptionListTerm>
              <DescriptionListDescription>
                {country.SurfaceArea?.toLocaleString()} km&sup2;
              </DescriptionListDescription>
            </DescriptionListGroup>
            {country.IndepYear && (
              <DescriptionListGroup>
                <DescriptionListTerm>Independence</DescriptionListTerm>
                <DescriptionListDescription>{country.IndepYear}</DescriptionListDescription>
              </DescriptionListGroup>
            )}
            {country.LifeExpectancy && (
              <DescriptionListGroup>
                <DescriptionListTerm>Life Expectancy</DescriptionListTerm>
                <DescriptionListDescription>
                  {country.LifeExpectancy} years
                </DescriptionListDescription>
              </DescriptionListGroup>
            )}
            {country.GNP != null && (
              <DescriptionListGroup>
                <DescriptionListTerm>GNP</DescriptionListTerm>
                <DescriptionListDescription>
                  ${country.GNP?.toLocaleString()}M
                </DescriptionListDescription>
              </DescriptionListGroup>
            )}
            {country.LocalName && country.LocalName !== country.Name && (
              <DescriptionListGroup>
                <DescriptionListTerm>Local Name</DescriptionListTerm>
                <DescriptionListDescription>{country.LocalName}</DescriptionListDescription>
              </DescriptionListGroup>
            )}
            <DescriptionListGroup>
              <DescriptionListTerm>Government</DescriptionListTerm>
              <DescriptionListDescription>{country.GovernmentForm}</DescriptionListDescription>
            </DescriptionListGroup>
            {country.HeadOfState && (
              <DescriptionListGroup>
                <DescriptionListTerm>Head of State</DescriptionListTerm>
                <DescriptionListDescription>{country.HeadOfState}</DescriptionListDescription>
              </DescriptionListGroup>
            )}
            {capital && (
              <DescriptionListGroup>
                <DescriptionListTerm>Capital</DescriptionListTerm>
                <DescriptionListDescription>
                  {capital.Name} ({capital.Population?.toLocaleString()})
                </DescriptionListDescription>
              </DescriptionListGroup>
            )}
          </DescriptionList>

          <Divider className="pf-v6-u-my-md" />
          {renderLanguagesPie(languages)}

          <Divider className="pf-v6-u-my-md" />
          {renderCitiesBar(cities, country.Capital)}
        </CardBody>
      </Card>
    );
  };

  const renderContinentResults = () => {
    if (!result || !result.length || queryType !== 'continent') return null;

    return (
      <>
        <Content>
          <strong>{result.length} countries in {continentInput}</strong>
        </Content>
        <div className="world-continent-grid">
          {result.map((country) => (
            <Card key={country.Code} isCompact>
              <CardBody>
                <Content>
                  <strong>{country.Name}</strong>{' '}
                  <Badge isRead>{country.Code}</Badge>
                </Content>
                <DescriptionList isHorizontal isCompact>
                  <DescriptionListGroup>
                    <DescriptionListTerm>Region</DescriptionListTerm>
                    <DescriptionListDescription>{country.Region}</DescriptionListDescription>
                  </DescriptionListGroup>
                  <DescriptionListGroup>
                    <DescriptionListTerm>Population</DescriptionListTerm>
                    <DescriptionListDescription>
                      {country.Population?.toLocaleString()}
                    </DescriptionListDescription>
                  </DescriptionListGroup>
                </DescriptionList>
                <Button
                  variant="link"
                  isInline
                  onClick={() => fetchCountryDetail(country.Name)}
                  className="pf-v6-u-mt-sm"
                >
                  View details
                </Button>
              </CardBody>
            </Card>
          ))}
        </div>
      </>
    );
  };

  const renderCityResults = () => {
    if (!result || !result.length || queryType !== 'city') return null;

    if (result.length === 1 && countryDetail) {
      return (
        <div className="world-city-detail-layout">
          <div>{renderCityCard(result[0], 0, 1)}</div>
          <div>{renderCountryCard()}</div>
        </div>
      );
    }

    if (result.length === 1) {
      return renderCityCard(result[0], 0, 1);
    }

    return result.map((item, index) => renderCityCard(item, index, result.length));
  };

  const masthead = (
    <Masthead>
      <MastheadMain>
        <MastheadBrand>
          <MastheadLogo>
            <GlobeIcon className="pf-v6-u-mr-sm" />
            World Database
          </MastheadLogo>
        </MastheadBrand>
      </MastheadMain>
    </Masthead>
  );

  return (
    <Page masthead={masthead}>
      <PageSection>
        <Content>
          <h1>World Database</h1>
          <p>Browse cities, countries, and continents from the world database.</p>
        </Content>
      </PageSection>
      <PageSection>
        <div className="world-query-globe-layout">
        <Card className="world-query-card">
          <CardTitle>Query</CardTitle>
          <CardBody>
            <Form
              onSubmit={(e) => {
                e.preventDefault();
                handleSubmit();
              }}
            >
              <FormGroup label="Query type" fieldId="query-type">
                <FormSelect
                  id="query-type"
                  value={queryType}
                  onChange={handleQueryTypeChange}
                >
                  <FormSelectOption value="city" label="City" />
                  <FormSelectOption value="country" label="Country" />
                  <FormSelectOption value="continent" label="Continent" />
                </FormSelect>
              </FormGroup>

              {queryType === 'continent' ? (
                <FormGroup label="Continent" fieldId="continent-select">
                  <FormSelect
                    id="continent-select"
                    value={continentInput}
                    onChange={(_event, value) => setContinentInput(value)}
                  >
                    {CONTINENTS.map((c) => (
                      <FormSelectOption key={c} value={c} label={c} />
                    ))}
                  </FormSelect>
                </FormGroup>
              ) : (
                <FormGroup label="Name" fieldId="query-input">
                  <TextInput
                    id="query-input"
                    type="text"
                    placeholder={`Enter a ${queryType} name`}
                    value={queryInput}
                    onChange={(_event, value) => setQueryInput(value)}
                    onKeyDown={handleKeyDown}
                  />
                </FormGroup>
              )}

              <Button variant="primary" onClick={handleSubmit} isDisabled={loading}>
                {loading ? <Spinner size="sm" /> : 'Search'}
              </Button>
            </Form>
          </CardBody>
        </Card>
        <GlobePanel lat={globeTarget.lat} lng={globeTarget.lng} label={globeTarget.label} />
        </div>

        {error && (
          <Alert variant="danger" title="Error" className="pf-v6-u-mt-lg" isInline>
            {error}
          </Alert>
        )}

        {(result || countryDetail) && (
          <div className="world-results">
            {queryType === 'city' && renderCityResults()}
            {queryType === 'country' && renderCountryCard()}
            {queryType === 'continent' && renderContinentResults()}
          </div>
        )}
      </PageSection>
    </Page>
  );
}

export default App;
