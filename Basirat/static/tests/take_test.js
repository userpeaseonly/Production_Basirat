setTimeout(function () {
    $("#test-information").hide();
    // Show all questions
    $("#questions").show();
}, 3000);

  // Set the duration in seconds
  const durationSeconds = test_duration_minutes * 60;

  // Function to update the timer display
  function updateTimer() {
      const currentTime = new Date().getTime();
      const endTime = startTime + durationSeconds * 1000;
      const remainingTime = Math.max(0, endTime - currentTime);
      const minutes = Math.floor(remainingTime / (1000 * 60));
      const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
      document.getElementById("timer").innerText = minutes + "m " + seconds + "s ";

      // If time is up, submit the answers
      if (remainingTime <= 0) {
          document.getElementById("testForm").submit();
      }
  }

  // Start the timer
  const startTime = new Date().getTime();
  updateTimer();
  setInterval(updateTimer, 1000); // Update timer every second


// Warning
$(window).on('beforeunload', function(){
    return "Any changes will be lost and your test will be broken!!!";
});

// Form Submit
$(document).on("submit", "form", function(event){
    // disable unload warning
    $(window).off('beforeunload');
});

$(window).on('beforeunload', function(event) {
    // Submit the form when leaving the page
    $('#testForm').submit();
});