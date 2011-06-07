function formatTime(date)
{
    var d = date.getHours()
    var m = date.getMinutes()
    return (d < 10 ? "0" + d : d) + ":" + (m < 10 ? "0" + m : m)
}

function addOption(selectElement, optionText, optionToSelect)
{                        
    var option = document.createElement("option")
    option.text = optionText
    try
    {
        // for IE earlier than version 8
        selectElement.add(option, selectElement.options[null])
    }
    catch (e)
    {
        selectElement.add(option, null);
    }
    if (optionText == optionToSelect)
        option.selected = true    
}

function initializeMonthDays(yearElementName, monthElementName, dayElementName, defaultDay)
{
    var selectYear = document.getElementsByName(yearElementName)[0]    
    var year = selectYear.options[selectYear.selectedIndex].text

    var selectMonth = document.getElementsByName(monthElementName)[0]    
    var month = selectMonth.selectedIndex

    var selectDay = document.getElementsByName(dayElementName)[0]
    for (var day = 1; day <= numberOfDaysInMonth(year, month); day++)
        addOption(selectDay, day, defaultDay);
}

function initializeTimeAndDate(yearElementName,
                               monthElementName,
                               dayElementName,
                               timeElementName,
                               defaultYear,
                               defaultMonth,      // month number!
                               defaultDay,
                               defaultTime)
{
    var selectYear = document.getElementsByName(yearElementName)[0]
    for (var year = 1990; year <= 2030; year++)
        addOption(selectYear, year, defaultYear)

    var selectMonth = document.getElementsByName(monthElementName)[0]
    for (var month = 0; month <= 11; month++)
        addOption(selectMonth, monthName[month], monthName[defaultMonth])

    initializeMonthDays(yearElementName, monthElementName, dayElementName, defaultDay);

    var inputTime = document.getElementsByName(timeElementName)[0]
    inputTime.value = defaultTime
}

function initializeContest(contestElementName, defaultContest)
{
    var selectContestType = document.getElementsByName(contestElementName)[0]
    var contestTypes = ["Training", "Championship", "Competition"]
    for (var i = 0; i < contestTypes.length; i++)
        addOption(selectContestType, contestTypes[i], defaultContest)    
}

function selectTimeZone(timeZoneElementName, defaultTimeZone)
{
    var selectTimeZone = document.getElementsByName(timeZoneElementName)[0]
    var options = selectTimeZone.options
    for (var i = 0; i < options.length; i++)
        if (options[i].text == defaultTimeZone)
            options[i].selected = true  
}

function onMonthChanged(yearElementName, monthElementName, dayElementName)
{
    var selectDay = document.getElementsByName(dayElementName)[0]
    var options = selectDay.options
    for (var i = options.length - 1; i >= 0; i--)
        selectDay.remove(i)

    initializeMonthDays(yearElementName, monthElementName, dayElementName, 1)
}

function getDateFromControls(yearElementName,
                             monthElementName,
                             dayElementName,
                             timeElementName)
{
    var selectYear = document.getElementsByName(yearElementName)[0]
    var year = parseInt(selectYear.options[selectYear.selectedIndex].text)

    var selectMonth = document.getElementsByName(monthElementName)[0]
    var month = selectMonth.selectedIndex

    var selectDay = document.getElementsByName(dayElementName)[0]
    var day = parseInt(selectDay.options[selectDay.selectedIndex].text)

    var time = document.getElementsByName(timeElementName)[0].value
    var hours = parseInt(time.substr(0, 2))
    var minutes = parseInt(time.substr(3, 2))

    return (0 <= hours && hours <= 23 && 0 <= minutes && minutes <= 59) ? new Date(year, month, day, hours, minutes, 0, 0) : null
}

function insertDateNames(tableId)
{
    var table = document.getElementById(tableId);
    var lastMonth = -1
    var lastDate = -1
    
    var i = 0
    while (i < table.rows.length)
    {
        var date = new Date(parseInt(table.rows[i].cells[0].innerHTML))
        if (date.getMonth() != lastMonth || date.getDate() != lastDate)
        {
            var row = table.insertRow(i)
            row.innerHTML = "<th colspan = 2 class = \"day_in_table\">" + date.getMonthName() + " " + date.getDate() + "</th>"
            lastMonth = date.getMonth()
            lastDate = date.getDate()
            i += 2
        }
        else
            i++   
    }
}