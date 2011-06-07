function onSubmit()
{
    var errors = document.getElementById("errors")
    errors.innerHTML = ""
    var result = true
        
    var full_name = document.getElementsByName("full_name")[0].value
    if (!full_name.length)
    {
        errors.innerHTML += "Full name should be non-empty <br>"
        result = false
    }
    if (full_name.length > 200)
    {
        errors.innerHTML += "Full name can't contain more than 200 symbols <br>"
        result = false
    }

    var short_name = document.getElementsByName("short_name")[0].value
    if (!short_name.length)
    {
        errors.innerHTML += "Short name should be non-empty <br>"
        result = false
    }

    var time = document.getElementsByName("time")[0].value
    if (!time.match(/^\d\d:\d\d$/))
    {
        errors.innerHTML += "Time should be in format HH:MM <br>"
        result = false
    }

    var h = parseInt(time.substr(0, 2))
    if (h >= 24)
    {
        errors.innerHTML += "Wrong time <br>"
        result = false
    }

    var m = parseInt(time.substr(3, 2))
    if (m >= 60)
    {
        errors.innerHTML += "Wrong time <br>"
        result = false
    }

    var home_page = document.getElementsByName("home_page")[0].value
    if (!home_page.match(/^http:\/\//) || home_page.indexOf(".") == -1)
    {
        errors.innerHTML += "Wrong home page url <br>"
        result = false
    }

    var info = document.getElementsByName("info")[0].value
    if (info.length > 1000)
    {
        errors.innerHTML += "Information can't contain more than 1000 symbols <br>"
        result = false        
    }

    return result
}

function onPostNumberSubmit()
{
    var postsToShow = document.getElementsByName("posts_to_show")[0].value
    var nPostsToShow = parseInt(postsToShow)
    if (nPostsToShow <   0 || nPostsToShow > 1000 || isNaN(nPostsToShow))
    {
        alert("Enter number from range 0..1000")
        return false
    }

    return true
}

function onMessageSubmit()
{
    var who = document.getElementsByName("who")[0].value
    if (who == "")
    {
        alert("Please, enter who you are")
        return false
    }

    var message = document.getElementsByName("content")[0].value
    if (message == "")
    {
        alert("Message must be non-empty")
        return false
    }
    if (message.length > 1000)
    {
        alert("Too large message")
        return false
    }

    return true
}