import React, { useEffect, useRef } from 'react';

function TextInput() {
    const countRef = useRef(2);

    const increment = () => {
      countRef.current += 1;
      console.log(countRef.current);
    };
  
    return <button onClick={increment}>Increment Count</button>;
  }

export default TextInput;