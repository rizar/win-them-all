function setLocalDates()
{
    var elements = /*document.*/getElementsByClassName("local_time")
    for (var i = 0; i < elements.length; i++)
        elements[i].innerHTML = new Date(parseInt(elements[i].innerHTML))

    elements = /*document.*/getElementsByClassName("local_hm")
    for (var i = 0; i < elements.length; i++)                                                        
        elements[i].innerHTML = formatTime(new Date(parseInt(elements[i].innerHTML)))
}                                                       

