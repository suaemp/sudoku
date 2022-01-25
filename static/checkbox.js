function addCheckboxEventListener() {
    document.getElementById("ranked").addEventListener('change', rankedCheckEvtListener)
}

function rankedCheckEvtListener(evt){
    let rankedCheckbox = evt.currentTarget
    let hintsCheckbox = document.getElementById("hints")
    let hintsLabel = document.getElementsByClassName('checkbox-label')[1]

    if (rankedCheckbox.checked) {
        hintsCheckbox.checked = false;
        hintsCheckbox.setAttribute('style', 'visibility: hidden')
        hintsLabel.setAttribute('style', 'visibility: hidden')
    } else {
        hintsCheckbox.setAttribute('style', 'visibility: visible')
        hintsLabel.setAttribute('style', 'visibility: visible')
    }
}

function setHintsCheckbox(){
    let rankedCheckbox = document.getElementById("ranked")
    let hintsCheckbox = document.getElementById("hints")
    let hintsLabel = document.getElementsByClassName('checkbox-label')[1]
    if (rankedCheckbox.checked) {
        hintsCheckbox.checked = false;
        hintsCheckbox.setAttribute('style', 'visibility: hidden')
        hintsLabel.setAttribute('style', 'visibility: hidden')
    }
}

addCheckboxEventListener()
setHintsCheckbox()