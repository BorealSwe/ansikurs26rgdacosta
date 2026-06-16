import React, { useRef, useEffect, useState } from 'react';
import Globe from 'react-globe.gl';

function GlobePanel({ lat, lng, label }) {
  const globeEl = useRef();
  const [marker, setMarker] = useState([]);

  useEffect(() => {
    if (!globeEl.current) return;
    const controls = globeEl.current.controls();
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.4;
    controls.enableZoom = false;
  }, []);

  useEffect(() => {
    if (lat == null || lng == null || !globeEl.current) return;

    globeEl.current.controls().autoRotate = false;
    globeEl.current.pointOfView({ lat, lng, altitude: 1.8 }, 1000);
    setMarker([{ lat, lng, label: label || '', size: 0.6, color: '#c9190b' }]);

    const timer = setTimeout(() => {
      if (globeEl.current) {
        globeEl.current.controls().autoRotate = true;
        globeEl.current.controls().autoRotateSpeed = 0.15;
      }
    }, 5000);

    return () => clearTimeout(timer);
  }, [lat, lng, label]);

  return (
    <div className="world-globe-container">
      <Globe
        ref={globeEl}
        width={380}
        height={380}
        globeImageUrl="/earth-blue-marble.jpg"
        backgroundColor="rgba(0,0,0,0)"
        showAtmosphere={true}
        atmosphereColor="#4394e5"
        atmosphereAltitude={0.15}
        pointsData={marker}
        pointLat="lat"
        pointLng="lng"
        pointColor="color"
        pointAltitude="size"
        pointRadius={0.5}
      />
    </div>
  );
}

export default GlobePanel;
