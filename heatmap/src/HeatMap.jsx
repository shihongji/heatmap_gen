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
            text: "Exercise",
            extraSelectionYears: 4,
          },
          guide: {
            enabled: false,
            showLessAndMoreLabels: false,
            colorRangeTogglesEnabled: false,
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
            text: "The day I have a run or a workout, I will mark it here.",
          },
          colorRanges: [
            {
              minimum: 1,
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
        fetch('heatmap_data.json')
            .then(response => response.json())
            .then(jsonData => {
                jsonData.data.forEach(item => {
                    let date = new Date(item.date * 1000);
                    $heat.addDate("heat-map-1", date, null, false);
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
          <h1 id="header">Heat.js - Basic</h1>
        </div>
  
        <div className="contents">
          <div id="heat-map-1" ref={heatMapRef}></div>
        </div>
      </div>
    );
  };

export default HeatMap;