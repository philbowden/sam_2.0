
let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
let days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
let day = document.getElementById("selectDay");
let dayIndex = getDayInt(day);

function getDayInt(day){
    for(let i = 0; i < days.length; i++){
        if (days[i] === day){
            return i;
        }
    }
}
if(day !== ''){
    displayDates(currentYear, currentMonth, dayIndex);
}

function getLessonDays(month, day) {
    let date = new Date(),
        lessonDays = [];

    while(date.getDay() !== day){
        date.setDate(date.getDate() + 1);
    }

    while (date.getMonth() === month){
        lessonDays.push(new Date(date.getTime()));
        date.setDate(date.getDate() + 7);
    }
    return lessonDays;

}
function  displayDates(year, month, day) {
    let idArray = ['lesson1', 'lesson2', 'lesson3','lesson4','lesson5'];
    let dates = getLessonDays(month, day);

}

function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    displayDates(currentMonth, currentYear);
}

function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    displayDates(currentMonth, currentYear);
}

function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    displayDates(currentMonth, currentYear);
}


/*
function getLessonDatesArray(day) {
            let lessonDatesArray = [];
            let date = new Date();
            let month = date.getMonth();
            while(date.getMonth() === month)
            if(date.getDay() === day) {
                lessonDatesArray.push(new Date(date));
            }
            date.setDate((date.getDate() + 1));
            return lessonDatesArray;
        }

function formatLessonDate(date) {
            let d = new Date(date),
                month = '' + (d.getMonth()),
                day = '' + d.getDate();
                let monthString = months[month];

            return [monthString, day].join('/');
        }*/
