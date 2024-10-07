import React, { useEffect, useRef } from 'react';
// import 'heat.js.css';

// Assuming that heat.min.js has been included in your public/index.html or is available as a global variable.
const HeatMap = () => {
    const heatMapRef = useRef(null);
  
    useEffect(() => {
      // Initialize heat map when component mounts
      if (heatMapRef.current) {
        const heatMapElement = heatMapRef.current;
        
        // Set up heat map configuration
        const heatMapConfig = {
          title: {
            text: "Focus Time",
            extraSelectionYears: 4,
          },
          guide: {
            enabled: true,
            showLessAndMoreLabels: true,
            colorRangeTogglesEnabled: true,
            showNumbersInGuide: true,
          },
          views: {
            map: {
                showMonthDayGaps: false,
                showDayNames: false,
            },
          },
          events: {
            onDayClick: onDayClick,
          },
          description: {
            text: "The data is tracked by the Forest App, starting from mid-September.",
          },
          colorRanges: [
            {
              minimum: 360,
              cssClassName: "day-color-1",
              mapCssClassName: "day-color-1",
              chartCssClassName: "chart-color-1",
              statisticsCssClassName: "statistics-color-1",
              tooltipText: "Day Color 1",
              visible: true,
            },
            {
              minimum: 420,
              cssClassName: "day-color-2",
              mapCssClassName: "day-color-2",
              chartCssClassName: "chart-color-2",
              statisticsCssClassName: "statistics-color-2",
              tooltipText: "Day Color 2",
              visible: true,
            },
            {
              minimum: 480,
              cssClassName: "day-color-3",
              mapCssClassName: "day-color-3",
              chartCssClassName: "chart-color-3",
              statisticsCssClassName: "statistics-color-3",
              tooltipText: "Day Color 3",
              visible: true,
            },            {
              minimum: 540,
              cssClassName: "day-color-4",
              mapCssClassName: "day-color-4",
              chartCssClassName: "chart-color-4",
              statisticsCssClassName: "statistics-color-4",
              tooltipText: "Day Color 4",
              visible: true,
            },
          ],
        };
  
        // Initialize heat map
        window.$heat.render(heatMapElement, heatMapConfig);
  
        // Add sample data
        fetch('focus_time.json')
            .then(response => response.json())
            .then(jsonData => {
                jsonData.data.forEach(item => {
                    let date = new Date(item.date * 1000);
                    $heat.addDate("heat-map-2", date, "focus", false);
                    $heat.updateDate("heat-map-2", date,  item.focus, "focus", false);
                });
                $heat.refreshAll();
            });
  
        // Refresh the heat map
        window.$heat.refreshAll();
      }
  
      // Cleanup function
      return () => {
        if (heatMapRef.current) {
          window.$heat.destroy(heatMapRef.current.id);
        }
      };
    }, []);
  
    const onDayClick = (date) => {
      console.log("Day clicked for: " + date.toString());
    };
  
    return (
      <div>
        <div className="header">
          <h1 id="header">Heat.js - Focus</h1>
        </div>
  
        <div className="contents">
          <div id="heat-map-2" ref={heatMapRef}></div>
        </div>
      </div>
    );
  };

export default HeatMap;