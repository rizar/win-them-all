monthName = ['January','February','March','April','May','June','July',
    'August','September','October','November','December'];

Date.prototype.getMonthName = function() 
{
    return monthName[this.getMonth()]
} 

nDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

function numberOfDaysInMonth(year, month)
{
    if (month != 1)
        return nDaysInMonth[month]
    else 
    {
        year = parseInt(year)
        if (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0))
            return 29
        else return 28
    }
}

Date.prototype.getNumberOfDaysInMonth = function()
{
    var month = this.getMonth()
    var year = this.getYear()
    return numberOfDaysInMonth(year, month)        
}