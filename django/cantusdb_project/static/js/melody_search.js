window.onload = melodySearch;
function melodySearch() {
    // `index` is the index of the currently active note slot, it starts from one
    var index = 1;
    // `notes` is a string consisting of all notes put on the canvas
    // it is updated with every call to `trackClick` or `deleteNotes`
    var notes = "";
    // `lastNote` stores the last entered note, it starts with empty str,
    // it is updated with every call to `trackClick` or `deleteNotes`
    var lastNote = "";
    // `anywhere` is true when "search anywhere" is checked, 
    // false when "search beginning" is checked
    var anywhere = false;
    // lastXhttp is a pointer to the last ajax request
    // if the user clicks on the canvas or deletes notes very fast, the older requests 
    // may not finish before the newer ones, causing the result table being updated multiple times, 
    // potentially with wrong results from the older requests
    // therefore we keep a pointer to the last request and abort it whenever sending a new request
    var lastXhttp = new XMLHttpRequest();
    const drawArea = document.getElementById("drawArea");
    const deleteOneButton = document.getElementById("deleteOne");
    const deleteAllButton = document.getElementById("deleteAll");
    const searchBeginButton = document.getElementById("searchBegin");
    const searchAnywhereButton = document.getElementById("searchAnywhere");
    const siglumField = document.getElementById("siglum");
    const resultsDiv = document.getElementById("resultsDiv");

    drawArea.addEventListener("mousemove", () => { trackMouse(index); });
    drawArea.addEventListener("click", trackClick);
    deleteOneButton.addEventListener("click", deleteOneNote);
    deleteAllButton.addEventListener("click", deleteAllNotes);
    searchBeginButton.addEventListener("click", searchBeginning);
    searchAnywhereButton.addEventListener("click", searchAnywhere);
    // for the search fields, search-as-you-type
    siglumField.addEventListener("input", search);

    function trackClick() {
        const y = event.pageY;
        // if click on the area without any notes, do nothing
        if (y < 256 || y >= 382) {
            return;
        }
        // otherwise, stop changing notes on the current slot
        drawArea.removeEventListener("mousemove", () => { trackMouse(index); })
        // add the note to the search term, according to the y position of the click
        if (index <= 14) {
            if (y < 264) {
                notes += "q";
            } else if (y < 272) {
                notes += "p";
            } else if (y < 279) {
                notes += "o";
            } else if (y < 287) {
                notes += "n";
            } else if (y < 294) {
                notes += "m";
            } else if (y < 302) {
                notes += "l";
            } else if (y < 309) {
                notes += "k";
            } else if (y < 317) {
                notes += "j";
            } else if (y < 324) {
                notes += "h";
            } else if (y < 332) {
                notes += "g";
            } else if (y < 339) {
                notes += "f";
            } else if (y < 347) {
                notes += "e";
            } else if (y < 354) {
                notes += "d";
            } else if (y < 362) {
                notes += "c";
            } else if (y < 369) {
                notes += "b";
            } else if (y < 377) {
                notes += "a";
            } else if (y < 382) {
                notes += "9";
            }

            // if the newly entered note is different from the last note
            if (notes.slice(-1) != lastNote) {
                // update `lastNote`
                lastNote = notes.slice(-1);
                // move focus to the next slot
                index = index + 1;
                drawArea.addEventListener("mousemove", () => { trackMouse(index); });
                // do the search
                search();
            } else {
                // if the newly entered note is the same as the last note, it's deemed invalid,
                // remove the newly entered note from `notes`
                notes = notes.slice(0, -1);
                return;
            }
        }
    }

    function trackMouse(noteIndex) {
        // console.log(event.type);
        // get the y coordinate of the mouse position, x doesn't matter
        // x = event.pageX;
        y = event.pageY;
        // console.log("X coords: " + x + ", Y coords: " + y);
        // compare it with the y coordinate of every staff line (hardcoded), 17 positions in total
        // staff line coordinates: [264, 279, 294, 309, 324, 339, 354, 369]
        if (document.getElementById(noteIndex)) {
            const currentPic = document.getElementById(noteIndex);
            // change the current image to the corresp. note image based on the y position
            if (y < 256) {
                currentPic.src = "/static/melody search tool/-.jpg";
            } else if (y < 264) {
                currentPic.src = "/static/melody search tool/b2.jpg";
            } else if (y < 272) {
                currentPic.src = "/static/melody search tool/a2.jpg";
            } else if (y < 279) {
                currentPic.src = "/static/melody search tool/g1.jpg";
            } else if (y < 287) {
                currentPic.src = "/static/melody search tool/f1.jpg";
            } else if (y < 294) {
                currentPic.src = "/static/melody search tool/e1.jpg";
            } else if (y < 302) {
                currentPic.src = "/static/melody search tool/d1.jpg";
            } else if (y < 309) {
                currentPic.src = "/static/melody search tool/c1.jpg";
            } else if (y < 317) {
                currentPic.src = "/static/melody search tool/b1.jpg";
            } else if (y < 324) {
                currentPic.src = "/static/melody search tool/a1.jpg";
            } else if (y < 332) {
                currentPic.src = "/static/melody search tool/g.jpg";
            } else if (y < 339) {
                currentPic.src = "/static/melody search tool/f.jpg";
            } else if (y < 347) {
                currentPic.src = "/static/melody search tool/e.jpg";
            } else if (y < 354) {
                currentPic.src = "/static/melody search tool/d.jpg";
            } else if (y < 362) {
                currentPic.src = "/static/melody search tool/c.jpg";
            } else if (y < 369) {
                currentPic.src = "/static/melody search tool/b.jpg";
            } else if (y < 377) {
                currentPic.src = "/static/melody search tool/a.jpg";
            } else if (y < 382) {
                currentPic.src = "/static/melody search tool/9.jpg";
            } else {
                currentPic.src = "/static/melody search tool/-.jpg";
            }
        }
    }

    // make an ajax call to the Django backend: do the search and return results
    function search() {
        // whenever a new search begins, abort the previous one, so that it does not update the result table with wrong data
        lastXhttp.abort()
        const xhttp = new XMLHttpRequest();
        // construct the ajax url with search parameters
        const url = new URL("/ajax/melody-search/", window.location.origin);
        url.searchParams.append("notes", notes);
        url.searchParams.append("anywhere", anywhere);
        url.searchParams.append("siglum", siglumField.value);

        xhttp.open("GET", url);
        xhttp.onload = function () {
            const data = JSON.parse(this.response)
            resultsDiv.innerHTML = `Search results <b>(${data.result_count} melodies)</b>`;
            resultsDiv.innerHTML += `<table id="resultsTable" class="table table-responsive table-sm small"><tbody></tbody></table>`;
            const table = document.getElementById("resultsTable").getElementsByTagName("tbody")[0];
            data.results.map(chant => {
                const newRow = table.insertRow(table.rows.length);
                newRow.innerHTML += `<td style="width:30%">
                                            <b>${chant.siglum}</b>
                                            <br>
                                            fol. <b>${chant.folio}</b>
                                            <br>
                                            <b>${chant.genre__name}</b> | Mode: <b>${chant.mode}</b>
                                    </td>`;
                newRow.innerHTML += `<td style="width:70%">
                                            <a href="${chant.chant_link}" target="_blank"><b>${chant.incipit}</b></a>
                                            <br>
                                            <div style="font-family: volpiano; font-size: 20px;">${chant.volpiano}</div>
                                            <br>
                                            ${chant.feast__name}
                                    </td>`
            });
            // hide the "updating results" prompt after loading the data
            document.getElementById("searchingPrompt").style.display = "none";
        }
        xhttp.onerror = function () {
            // handle errors
            document.getElementById("resultsDiv").innerHTML = "ajax error"
        }
        xhttp.send();
        // update the pointer to the last xhttp request
        lastXhttp = xhttp;
        // display the "updating results" prompt after sending the ajax request
        document.getElementById("searchingPrompt").style.display = "inline";
    }

    function deleteOneNote() {
        document.getElementById(index - 1).src = "/static/melody search tool/-.jpg";
        // set the focused slot back one unit
        index = index - 1;
        // remove the last character from the search term
        notes = notes.slice(0, -1);
        // redo the search using updated notes
        if (notes != "") {
            // update `lastNote`
            lastNote = notes.slice(-1);
            search();
        }
        // if there's no notes left
        else {
            // set index back to the beginning
            index = 1;
            // set `lastNote` back to empty
            lastNote = "";
            // abort the last ajax request, so that it does not populate the result table
            lastXhttp.abort();
            // hide the "updating results" prompt
            document.getElementById("searchingPrompt").style.display = "none";
            // clear the search results
            resultsDiv.innerHTML = "";
        }
    }

    function deleteAllNotes() {
        for (let i = 1; i < index; i++) {
            document.getElementById(i).src = "/static/melody search tool/-.jpg";
        }
        // set the focused slot to the beginning
        index = 1;
        // set `lastNote` back to empty
        lastNote = "";
        // set the search term to empty
        notes = "";
        // abort the last ajax request, which, if unfinished, could populate the result table even after deleting all notes
        lastXhttp.abort();
        // hide the "updating results" prompt
        document.getElementById("searchingPrompt").style.display = "none";
        // clear the search results
        resultsDiv.innerHTML = "";
    }

    function searchBeginning() {
        // do nothing if "search beginning" is already checked
        if (anywhere) {
            anywhere = false;
            if (notes != "") {
                search();
            }
        }
    }

    function searchAnywhere() {
        // do nothing if "search anywhere" is already checked
        if (anywhere == false) {
            anywhere = true;
            if (notes != "") {
                search();
            }
        }
    }

    function showCoords() {
        var x = event.pageX;
        var y = event.pageY;
        var coords = "X coords: " + x + ", Y coords: " + y;
        console.log(coords);
    }
}
