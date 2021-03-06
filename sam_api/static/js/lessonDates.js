 let today = new Date();
 let currentDay = today.getDay();
 let currentMonth = today.getMonth();
 let currentYear = today.getFullYear();

 let days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];

function resetDay(dayNumber)
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

 function displayDates(year, month, dayNumber)
 {
     let monthString = formatFullMonth(month);
     document.getElementById('currentdate').innerHTML = monthString + "  " + year;
     let date_label_ids = ['lesson1', 'lesson2', 'lesson3','lesson4','lesson5'];
     let dates = getLessonDays(year, month, dayNumber);
     let currentNumColumns = (document.getElementById('adminTable').rows[0].cells.length) - 2;
     let numLessonDays = dates.length;
     optimizeTable(currentNumColumns, numLessonDays);
     let index = 0;
     while(dates[index] != null)
     {
         let monthAbbreviation = dates[index].getUTCMonth();
         monthAbbreviation = formatMonthAbriviation(monthAbbreviation);
         let day = dates[index].getDate();
         let id = date_label_ids[index];
         document.getElementById(id).innerHTML = monthAbbreviation + " " + day;
         index++;
     }
 }

 function optimizeTable(currentNumColumns, numLessonDays)
 {
    let rows = document.getElementsByTagName('tr');
    if(currentNumColumns === 5 && numLessonDays ===4)
    {
        for(let i = 0; i < rows.length; i++)
        {
            rows[i].lastChild.remove();
        }
    }
    else if(currentNumColumns=== 4 && numLessonDays ===5)
    {
        let th = document.createElement('th');
        th.setAttribute("id", "lesson5");
        th.setAttribute("class", "text-center");
        rows[0].appendChild(th);
        for(let i = 1; i < rows.length-1; i++)
        {
            rows[i].insertCell(-1);
        }
    }
 }



 function formatMonthAbriviation(date)
 {
     let months = ["Jan ", "Feb ", "Mar ", "Apr ", "May ", "June ", "July ", "Aug ", "Sept ", "Oct ", "Nov ", "Dec "];
     return months[date];
 }
 function formatFullMonth(date)
 {
     let months = ["January ", "February ", "March ", "April ", "May ", "June ", "July ", "August ", "September ", "October ", "November ", "December "];
     return months[date];
 }


 function nextMonth()
 {
     currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
     currentMonth = (currentMonth + 1) % 12;
     console.log("currentYear: " + currentYear + " currentMonth: " + currentMonth);
     displayDates(currentYear, currentMonth, currentDay);
 }

 function previousMonth()
 {
     currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
     currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
     console.log("currentYear: " + currentYear + " currentMonth: " + currentMonth);
     displayDates(currentYear, currentMonth, currentDay);
 }




