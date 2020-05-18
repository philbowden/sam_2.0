 let today = new Date();
 let currentDay = today.getDay();
 let currentMonth = today.getMonth();
 let currentYear = today.getFullYear();

 let days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",""];

function setDay(dayNumber)
{
    displayDates(currentYear, currentMonth, dayNumber);
}

 function getDayInt(day)
 {
     let index = 0;
     while(days[index] !== day)
     {
         index++;
     }
     return index;
 }

 function getLessonDays(year, month, dayNumber)
 {
   let firstDayOfThisMonth = new Date(year, month, 1);
   let firstDayOfThisMonthIndex = firstDayOfThisMonth.getDay();
   let dates = [];
   let daysToFirst = (dayNumber + 7 - firstDayOfThisMonthIndex) % 7;
   let firstOf = new Date(firstDayOfThisMonth.setDate(firstDayOfThisMonth.getDate() + daysToFirst));

   while (firstOf.getMonth() === month)
   {
     dates.push(new Date(+firstOf));
     firstOf.setDate(firstOf.getDate() + 7);
   }
   return dates;
 }
 function displayDates(year, month, day)
 {
     let date_label_ids = ['lesson1', 'lesson2', 'lesson3','lesson4','lesson5'];
     let dates = getLessonDays(year, month, day);
     let index = 0;
     while(dates[index] != null)
     {
         let month = dates[index].getUTCMonth();
         month = formatMonth(month);
         let day = dates[index].getDate();
         let id = date_label_ids[index];
         document.getElementById(id).innerHTML = month + " " + day;
         index++;
     }
     if(dates.length < 5) delete5thLessonDayColumn()
 }

 function delete5thLessonDayColumn()
 {
    let allRows = document.getElementById("adminTable").rows;
         for (let i=0; i< allRows.length; i++)
         {
             allRows[i].deleteCell(-1);
         }
 }

 function formatMonth(date)
 {
     let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
     return months[date];
 }

 function next()
 {
     currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
     currentMonth = (currentMonth + 1) % 12;
     displayDates(currentMonth, currentYear, currentDay);
 }

 function previous()
 {
     currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
     currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
     displayDates(currentMonth, currentYear, currentDay);
 }

 function jump()
 {
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
