// הפונקציה היחידה נותרה - עדכון שכבות התמונה וטקסט השנה מהשרת.
function updateDisplay() {
    // קורא לשרת הפייתון בכתובת /get_current_data
    fetch('/get_current_data')
        .then(response => response.json())
        .then(data => {
            // עדכון שכבות עיקריות
            document.getElementById('second-layer').src = data.second_image;
            document.getElementById('minute-layer').src = data.minute_image;
            document.getElementById('hour-layer').src = data.hour_image;
            
            // עדכון שכבות מילוי תמונה (יום וחודש)
            document.getElementById('day-fill-layer').src = data.day_image;
            document.getElementById('month-fill-layer').src = data.month_image;
            
            // עדכון טקסט השנה
            document.getElementById('year-text-layer').textContent = data.year_text;
        })
        .catch(error => {
            console.error('Error fetching time data:', error);
            document.getElementById('year-text-layer').textContent = 'שגיאת טעינה!';
        });
}

// קריאה ראשונית:
updateDisplay(); 

// הפעלת עדכון השרת כל שנייה
setInterval(updateDisplay, 1000);
