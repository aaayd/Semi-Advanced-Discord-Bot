var allChanges = {}
var selected_channel_id

document.getElementById("defaultTab").click();

function openTab(evt, cityName) {
  var i, tabcontent, tablinks;
  
  tabcontent = document.getElementsByClassName("tabcontent");
  
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

function scrollToText(name) {
  var str_array = name.split(" ")
  var new_str = ""

  for(var i=0; i<str_array.length; i++)
  {
    if (str_array[i] == ""){
      continue;
    }

    if (str_array[i] == "AFK" || str_array[i] == "XP" ){
      new_str = str_array[i]
      break;
    }
    new_str += str_array[i][0].toUpperCase() + str_array[i].substr(1).toLowerCase() + " ";
  }
  new_str = new_str.trim()

  $(window).scrollTop($(`*:contains('${new_str}'):last`).offset().top);
}
            
function filterTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("warn-table-filter");
    filter = input.value.toUpperCase();
    table = document.getElementById("warn-table");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
            
function selectChannel(id, name) {
    dropdown_button = document.getElementById("channel-dropdown-button")

    dropdown_button.textContent = name
    
    selected_channel_id = id

}
            
function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("warn-table");
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /*check if the two rows should switch place,
            based on the direction, asc or desc:*/
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            //Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /*If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again.*/
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}
            
function updateCommandActivityState(id) {
    var checkBox = document.getElementById(id);
    var cardBox = document.getElementById(`card_${id}`);
    if (id in allChanges)
        delete allChanges[id]
    
    if (checkBox.checked == true){
        allChanges[id] = 1

        
        cardBox.style.backgroundColor="#111213"
    }
        
    else {
        allChanges[id] = 0
        cardBox.style.backgroundColor="#202121"
    }
    
}

