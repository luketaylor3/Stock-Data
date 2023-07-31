console.log("hello");
let select = document.getElementById("select");
let list = document.getElementById("list");
let selectText = document.getElementById("selectText");
let options = document.getElementsByClassName("options");
let inputField = document.getElementById("inputField");



// category select
select.onclick = function(){
    list.classList.toggle("open");
}

for(option of options){
    option.onclick = function(){
        selectText.innerHTML = this.innerHTML;
        if (selectText.innerHTML == "S&amp;P 500"){
            inputField.placeholder = "Search in S&P 500";
        }
        else{
            inputField.placeholder = "Search in " + selectText.innerHTML;
        }
        
    }
}



// search button
const searchButton = $("#submit");


searchButton.on("click", function() {
    searchButton.addClass("clicked");
    setTimeout(() => {
        searchButton.removeClass("clicked");
    }, 300);
});





// search box

var input = $("#inputField");
var results = $("#results");
var searchRegion = $("#searchDiv");





// closes search suggestions
$(document).on("click", function(event) {
    if (!searchRegion.is(event.target) && searchRegion.has(event.target).length === 0){
        results.empty();
    }
})

// gets list being worked with
function getCategory(){
    switch ($("#selectText").text()) {
        case "All categories":
            return combined;
        case "S&amp;P 500":
            return combined;
        case "Nasdaq 100":
            return nas;
        case "Dow Jones":
            return dow;
        default:
            return combined;
    }
}

// produces suggestions 
function getSuggestions(query){
    return getCategory().filter(function(item){
        return item.toLowerCase().startsWith(query);
    });
}

// displays suggestions
function showSuggestions(matches){
    results.empty()
    let count = 0;
    matches.forEach(function(match) {
        if (count < 5){
            var listItem = $("<li>").text(match);
            results.append(listItem);
            count++;
        }
    })
}

// handles input change
input.on("input", function(){
    var query = $(this).val().toLowerCase();
    var matches = getSuggestions(query);
    showSuggestions(matches);
});


// handles suggestion click
results.on("click", "li", function() {
    var selectedValue = $(this).text();
    input.val(selectedValue);
    results.empty();
});

// handles suggestion hover
results.on("mouseenter", "li", function(){
    $(this).addClass("hovered");
}).on("mouseleave", "li", function() {
    $(this).removeClass("hovered");
});








