// Async Script Loader - Prevents long main thread tasks
(function() {
  'use strict';

  // Break up long tasks using requestIdleCallback
  function runWhenIdle(callback) {
    if ('requestIdleCallback' in window) {
      requestIdleCallback(callback, {timeout: 2000});
    } else {
      setTimeout(callback, 1);
    }
  }

  // Defer non-critical scripts
  function deferScript(src, callback) {
    runWhenIdle(function() {
      const script = document.createElement('script');
      script.async = true;
      script.defer = true;
      script.src = src;
      if (callback) script.onload = callback;
      document.body.appendChild(script);
    });
  }

  // Load third-party scripts only when needed
  window.loadThirdParty = function() {
    // Add any third-party scripts here
  };

  // Break up initialization into chunks
  function initializeInChunks() {
    const tasks = [];

    // Add initialization tasks here
    tasks.forEach((task, index) => {
      setTimeout(task, index * 50); // Spread tasks over time
    });
  }

  // Start after page load
  if (document.readyState === 'complete') {
    initializeInChunks();
  } else {
    window.addEventListener('load', initializeInChunks);
  }
})();