exports.city = (db) => {
    return (req, res) => {
        const cityName = req.query.name;

        if (!cityName) {
            return res.status(400).send('Missing city name in query parameters.');
        }

        const sql = 'SELECT * FROM city WHERE LOWER(Name) = LOWER(?)';
        db.query(sql, [cityName], (err, result) => {
            if (err) throw err;
            res.send(result);
        });
    };
};

exports.country = (db) => {
    return (req, res) => {
        const countryName = req.query.name;

        if (!countryName) {
            return res.status(400).send('Missing country name in query parameters.');
        }

        const sql = 'SELECT * FROM country WHERE LOWER(Name) = LOWER(?)';
        db.query(sql, [countryName], (err, result) => {
            if (err) throw err;
            res.send(result);
        });
    };
};

exports.languages = (db) => {
    return (req, res) => {
        const code = req.query.code;

        if (!code) {
            return res.status(400).json({ message: 'Missing country code in query parameters.' });
        }

        const sql = 'SELECT * FROM countrylanguage WHERE CountryCode = ? ORDER BY Percentage DESC';
        db.query(sql, [code], (err, result) => {
            if (err) throw err;
            res.json(result);
        });
    };
};

exports.countryCities = (db) => {
    return (req, res) => {
        const code = req.query.code;

        if (!code) {
            return res.status(400).json({ message: 'Missing country code in query parameters.' });
        }

        const sql = 'SELECT * FROM city WHERE CountryCode = ? ORDER BY Population DESC LIMIT 10';
        db.query(sql, [code], (err, result) => {
            if (err) throw err;
            res.json(result);
        });
    };
};

exports.continent = (db) => {
    return (req, res) => {
        const name = req.query.name;

        if (!name) {
            return res.status(400).json({ message: 'Missing continent name in query parameters.' });
        }

        const sql = 'SELECT * FROM country WHERE Continent = ? ORDER BY Population DESC';
        db.query(sql, [name], (err, result) => {
            if (err) throw err;
            res.json(result);
        });
    };
};

exports.countryDetail = (db) => {
    return (req, res) => {
        const countryName = req.query.name;
        const countryCode = req.query.code;

        if (!countryName && !countryCode) {
            return res.status(400).json({ message: 'Missing country name or code in query parameters.' });
        }

        const countrySql = countryCode
            ? 'SELECT * FROM country WHERE Code = ?'
            : 'SELECT * FROM country WHERE LOWER(Name) = LOWER(?)';
        db.query(countrySql, [countryCode || countryName], (err, countries) => {
            if (err) throw err;
            if (!countries.length) {
                return res.json([]);
            }

            const country = countries[0];
            const code = country.Code;

            const langSql = 'SELECT * FROM countrylanguage WHERE CountryCode = ? ORDER BY Percentage DESC';
            const citiesSql = 'SELECT * FROM city WHERE CountryCode = ? ORDER BY Population DESC LIMIT 10';
            const capitalSql = 'SELECT * FROM city WHERE ID = ?';

            db.query(langSql, [code], (err, languages) => {
                if (err) throw err;

                db.query(citiesSql, [code], (err, cities) => {
                    if (err) throw err;

                    db.query(capitalSql, [country.Capital], (err, capitalResult) => {
                        if (err) throw err;

                        res.json({
                            country,
                            languages,
                            cities,
                            capital: capitalResult[0] || null
                        });
                    });
                });
            });
        });
    };
};
