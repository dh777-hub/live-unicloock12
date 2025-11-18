from flask import Flask, jsonify, render_template
import datetime
from decimal import Decimal, getcontext
from fractions import Fraction

app = Flask(__name__)
# הגדרת דיוק גבוה לחישובים (כדי למנוע טעויות עיגול ב-Decimal)
getcontext().prec = 100

def base_conversion(value, year_value=None):
    """
    ממיר את ערך השנה לבסיס 12 ומחזיר את הספרות מופרדות ברווח.
    (כולל תיקון להיפוך סדר הספרות).
    """
    
    if value == 'YEAR_TEXT':
        if year_value is None:
            return 'ERROR' 

        res = Fraction(year_value)
        num_digits = 1
        digits = []
        
        # חישוב ספרות בבסיס 12
        while res > 12:
            res /= 12
            num_digits += 1
        for i in range(num_digits):
            digits.append(int(res))
            res = (res - int(res)) * 12
        
        # טיפול במקרי אפסים או ספריות
        while 0 in digits[1:]:
            for i in range(num_digits - 1):
                if digits[i + 1] == 0:
                    digits[i] -= 1
                    digits[i + 1] = 12
        if digits[0] == 0 and len(digits) > 1:
            digits.pop(0)
            
        # תיקון סדר הספרות
        digits.reverse() 
        
        return ' '.join(map(str, digits))

    # עבור אינדקסים (second_index, minute_index וכו') - ברירת מילון
    if int(value) == value and value > 0:
        return int(value)
    
    return 1

def calculate_unique_time_data():
    """
    מחשב את 5 האינדקסים הייחודיים ומחזיר את הנתונים.
    """

    seconds_since_big_bang = Decimal('466576794025624028')
    reference_time = datetime.datetime(2020, 12, 31, 23, 59, 59)
    input_time = datetime.datetime.utcnow()
    second_multiplier = Decimal('285738202.060366731702559') / Decimal('299792458')

    difference_in_seconds = (input_time - reference_time).total_seconds()
    total_seconds = Decimal(difference_in_seconds) + seconds_since_big_bang
    new_total_seconds = total_seconds * second_multiplier

    # --- חישוב שנייה (1-72) ---
    new_total_min = new_total_seconds / 72
    new_seconds = round((new_total_min - int(new_total_min)) * 72)
    second_index = int(new_seconds) if new_seconds > 0 else 72

    # --- חישוב דקה (1-54) ---
    new_total_hours = Decimal(int(new_total_min)) / 54
    new_minutes = round((new_total_hours - int(new_total_hours)) * 54)
    minute_index = int(new_minutes) if new_minutes > 0 else 54

    # --- חישוב שעה (1-24) ---
    new_total_days = Decimal(int(new_total_hours)) / 24
    new_hours = round((new_total_days - int(new_total_days)) * 24)
    hour_index = int(new_hours) if new_hours > 0 else 24

    # --- חישוב יום ייחודי (1-36) ---
    new_total_months = Decimal(int(new_total_days)) / 36
    new_days = round((new_total_months - int(new_total_months)) * 36) + 1
    day_index = int(new_days) if new_days > 0 else 36

    # --- חישוב חודש ייחודי (1-12) ---
    new_total_years = Decimal(int(new_total_months)) / 12
    new_months = round((new_total_years - int(new_total_years)) * 12) + 1
    month_index = int(new_months) if new_months > 0 else 12

    # --- חישוב השנה החדשה והפלט הטקסטואלי ---
    new_years = int(new_total_years)
    unique_year_output = base_conversion('YEAR_TEXT', year_value=new_years) 

    return {
        'second_image': f'/static/images/{second_index}s.png',
        'minute_image': f'/static/images/{minute_index}d.png',
        'hour_image': f'/static/images/{hour_index}h.png',
        
        'day_image': f'/static/images/{day_index}m.png',  
        'month_image': f'/static/images/{month_index}i.png', 
        
        'year_text': unique_year_output 
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_current_data')
def get_current_data():
    data = calculate_unique_time_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
