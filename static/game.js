let selected_tool = 0
let selected_number = null
let selected_field_index = null
let found_numbers = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}
const timerInterval = setInterval(Timer, 1000) //consider refactoring
let elapsed_time = game_data['elapsed_time']


function addToolButtonsEventListeners() {
    document.getElementsByClassName('pen-button')[0].addEventListener('click', selectPenListener);
    document.getElementsByClassName('pencil-button')[0].addEventListener('click', selectPencilListener);
    document.getElementsByClassName('eraser-button')[0].addEventListener('click', selectEraserListener);
}

function selectPenListener(){
    if (selected_tool !== 0){
        selected_tool = 0;
        document.getElementsByClassName("pen-button")[0].id = 'selected';
        document.getElementsByClassName("pencil-button")[0].id = 'deselected';
        document.getElementsByClassName("eraser-button")[0].id = 'deselected';
        for (let i = 0; i < 9; i++){
            let numberButton = document.getElementsByClassName("number-button")[i]
            if (numberButton.id !== 'hoverable-selected-number-button'){
                numberButton.id = 'hoverable-number-button';
            }
        }
        deactivateFoundNumberButtons();
    }
}

function selectPencilListener(){
    if (selected_tool !== 1) {
        selected_tool = 1;
        document.getElementsByClassName("pen-button")[0].id = 'deselected';
        document.getElementsByClassName("pencil-button")[0].id = 'selected';
        document.getElementsByClassName("eraser-button")[0].id = 'deselected';
        for (let i = 0; i < 9; i++) {
            let numberButton = document.getElementsByClassName("number-button")[i]
            if (numberButton.id !== 'hoverable-selected-number-button'){
                numberButton.id = 'hoverable-number-button';
            }
        }
        deactivateFoundNumberButtons();
    }
}

function selectEraserListener(){
    if (selected_tool !== 2) { //const for tools
        selected_tool = 2;
        document.getElementsByClassName("pen-button")[0].id = 'deselected';
        document.getElementsByClassName("pencil-button")[0].id = 'deselected';
        document.getElementsByClassName("eraser-button")[0].id = 'selected';
        selected_number = null
        deactivateNumberButtons()
        deselectAllFields()
    }
}

function addNumberButtonsEventListeners() {
    for (let i = 0; i < 9; i++){
        let number_button = document.getElementsByClassName('number-button')[i]
        number_button.number = i+1
        number_button.addEventListener('click', selectNumberListener);
    }
}

function selectNumberListener(evt) {
    let number_button = evt.target;
    numberButtonAction(number_button)
}


function addKeyboardEventListeners(){
    document.addEventListener('keydown', keyboardKeyListener)
}


function keyboardKeyListener(event) {
    let functionKeys = [' ', 'z', 'x', 'c', 'Escape'];
    let arrowKeys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];
    if (arrowKeys.includes(event.key)) {
        for (let i = 0; i < 4; i++) {
            if (event.key === arrowKeys[i]) {
                arrowNavigate(i)
            }
        }

    } else if (functionKeys.includes(event.key)) {
        if (event.key === ' '){
            spaceBarAction();
        } else if (event.key === 'z'){
            selectPenListener();
        } else if (event.key === 'x'){
            selectPencilListener();
        } else if (event.key === 'c'){
            selectEraserListener();
        } else {
            deselectAllFields();
        }

    } else {
        for (let i = 0; i < 9; i++) {
            if (event.key === (i + 1).toString()) {
                let number_button = document.getElementsByClassName('number-button')[i];
                numberButtonAction(number_button);
            }
        }
    }
    deactivateFoundNumberButtons();
}

function arrowNavigate(direction){
    if (selected_field_index === null) {
        selected_field_index = ['4', '4'];
    } else {
        setSelectedFieldIndex(direction);
    }
    selected_number = null;
    for (let i = 0; i < 9; i++){
        if (selected_tool !== 2) {
            document.getElementsByClassName('number-button')[i].id = 'hoverable-number-button';
        }
    }
    let tile = getFieldElementByRowCol(selected_field_index[0], selected_field_index[1]);
    tile.parentElement.id = 'selected-tile-border';
    if (tile.id !== 'mistake-tile') {
        if (tile.id === 'initial-val-tile') {
            tile.id = 'selected-initial-val-tile';
        } else if (tile.id !== 'selected-initial-val-tile') {
            tile.id = 'selected-tile';
        }
    }
    for (let j = 0; j < 81; j++) {
        setFieldSelection(j);
    }
    selectAllQuadrantFields(tile.parentElement);
}

function spaceBarAction(){
    if (selected_field_index !== null) {
        let tile = getFieldElementByRowCol(selected_field_index[0], selected_field_index[1]);
        if (tile.id !== 'selected-initial-val-tile') {
            eraseField(tile);
        }
    }
}

function setSelectedFieldIndex(direction){
    let currentRow = parseInt(selected_field_index[0])
    let currentCol = parseInt(selected_field_index[1])
    if (direction === 0){
        if (currentRow === 0){
            currentRow = '8';
        } else {
            currentRow = (currentRow - 1).toString()
        }
        currentCol = currentCol.toString();
    } else if (direction === 1){
        if (currentRow === 8){
            currentRow = '0';
        } else {
            currentRow = (currentRow + 1).toString()
        }
        currentCol = currentCol.toString();
    } else if (direction === 2){
        if (currentCol === 0){
            currentCol = '8';
        } else {
            currentCol = (currentCol - 1).toString()
        }
        currentRow = currentRow.toString();
    } else if (direction === 3){
        if (currentCol === 8){
            currentCol = '0';
        } else {
            currentCol = (currentCol + 1).toString()
        }
        currentRow = currentRow.toString();
    }
    selected_field_index = [currentRow, currentCol]
}


function numberButtonAction(number_button){
    if (number_button.id !== 'inactive-number-button' && selected_field_index === null) {
        for (let j = 0; j < 9; j++) {
            document.getElementsByClassName('number-button')[j].id = 'hoverable-number-button'
        }
        deselectAllFields()

        if (selected_number !== number_button.number) {
            selected_number = number_button.number;
            number_button.id = 'hoverable-selected-number-button';
            selectAllSameNumberFields();
        } else {
            selected_number = null
        }

    } else if (number_button.id !== 'inactive-number-button') {
        let selected_tile = getSelectedFieldElement()
        if (selected_tile.id !== 'selected-initial-val-tile') {
            if (selected_tool === 0) {
                markFieldWithPen(number_button.number, selected_tile)
            } else {
                markFieldWithPencil(number_button.number, selected_tile, true)
            }
        }
    }
    deactivateFoundNumberButtons();
}


function addBoardFieldEventListeners(){
    for (let i = 0; i < 81; i++){
        let field = document.getElementsByClassName('tile-border')[i];
        field.number = i
        document.getElementsByClassName('tile-border')[i].addEventListener('click', selectFieldEventListener);
    }
}

function selectFieldEventListener(evt){
    let tile = evt.currentTarget;
    let selected_row = tile.dataset.tilerow;
    let selected_col = tile.dataset.tilecol;
    if (selected_tool !== 2){
        if ((selected_field_index === null) || ((selected_row !== selected_field_index[0]) || (selected_col !== selected_field_index[1]))) {
            selected_field_index = [selected_row, selected_col]

            if (selected_number === null) {
                tile.id = 'selected-tile-border'

                for (let j = 0; j < 81; j++) {
                    setFieldSelection(j)
                }
                selectAllQuadrantFields(tile)

            } else {
                if ((tile.firstElementChild.id !== 'selected-initial-val-tile') && (tile.firstElementChild.id !== 'initial-val-tile')) {
                    if (selected_tool === 0) {
                        markFieldWithPen(selected_number, tile.firstElementChild)
                        selectAllSameNumberFields()
                    } else {
                        markFieldWithPencil(selected_number, tile.firstElementChild, true)
                    }
                }
                selected_field_index = null
            }
        } else {
            deselectAllFields()
        }
    } else {
        if ((tile.firstElementChild.id !== 'initial-val-tile') && (tile.firstElementChild.id !== 'selected-initial-val-tile')){
            selected_field_index = [selected_row, selected_col]
            eraseField(tile.firstElementChild);
            deselectAllFields();
            selected_field_index = null;
        }
    }
    deactivateFoundNumberButtons();
}

function setFieldSelection(fieldNo){
    let iter_tile = document.getElementsByClassName('tile-border')[fieldNo]
    let iter_tile_row = iter_tile.dataset.tilerow
    let iter_tile_col = iter_tile.dataset.tilecol

    if ((selected_field_index === null) || ((iter_tile_row !== selected_field_index[0]) || (iter_tile_col !== selected_field_index[1]))) {
        document.getElementsByClassName('tile-border')[fieldNo].id = '';
    }
    if ((selected_field_index === null) || ((iter_tile_row !== selected_field_index[0]) && (iter_tile_col !== selected_field_index[1]))) {
        if ((iter_tile.firstElementChild.id === 'initial-val-tile') || (iter_tile.firstElementChild.id === 'selected-initial-val-tile')) {
            iter_tile.firstElementChild.id = 'initial-val-tile';
        } else if (iter_tile.firstElementChild.id !== 'mistake-tile') {
            iter_tile.firstElementChild.id = '';
        }

    } else {
        if ((iter_tile.firstElementChild.id === 'initial-val-tile') || (iter_tile.firstElementChild.id === 'selected-initial-val-tile')) {
            iter_tile.firstElementChild.id = 'selected-initial-val-tile';
        } else if (iter_tile.firstElementChild.id !== 'mistake-tile'){
            iter_tile.firstElementChild.id = 'selected-tile';
        }
    }
}

function selectAllQuadrantFields(tile){
    let gridItems = tile.parentElement.parentElement;
    for (let i=0; i < 9; i++){
        let boardTile = gridItems.children[i].firstElementChild.firstElementChild;
        if (boardTile.id === 'initial-val-tile') {
            boardTile.id = 'selected-initial-val-tile';
        } else if (boardTile.id === ''){
            boardTile.id = 'selected-tile';
        }
    }
}

function selectAllSameNumberFields(){
    for (let i=0; i < 81; i++){
        let boardTile = document.getElementsByClassName('board-tile')[i];
        if (selected_number === parseInt(boardTile.innerHTML)){
            if (boardTile.id === 'initial-val-tile') {
                boardTile.id = 'selected-initial-val-tile';
            } else if (boardTile.id === ''){
                boardTile.id = 'selected-tile';
            }
        }
    }
}

function deselectAllFields(){
    selected_field_index = null
    for (let i = 0; i < 81; i++){
        let iter_tile = document.getElementsByClassName('tile-border')[i]
        iter_tile.id = ''
        if ((iter_tile.firstElementChild.id === 'initial-val-tile') || (iter_tile.firstElementChild.id === 'selected-initial-val-tile')) {
            iter_tile.firstElementChild.id = 'initial-val-tile';
        } else if (iter_tile.firstElementChild.id !== 'mistake-tile') {
            iter_tile.firstElementChild.id = '';
        }
    }
}

function removeAllEventListeners(){
    document.getElementsByClassName('pen-button')[0].removeEventListener('click', selectPenListener);
    document.getElementsByClassName('pencil-button')[0].removeEventListener('click', selectPencilListener);
    document.getElementsByClassName('eraser-button')[0].removeEventListener('click', selectEraserListener);

    let number_buttons = document.getElementsByClassName('number-button')
    for (let i = 0; i < number_buttons.length; i++) {
        let element = number_buttons[i];
        element.removeEventListener('click', selectNumberListener);
    }

    let fields = document.getElementsByClassName('tile-border')
    for (let i = 0; i < fields.length; i++) {
        let element = fields[i];
        element.removeEventListener('click', selectFieldEventListener);
    }
}

function deactivateNumberButtons(){
    for (let i = 0; i < 9; i++) {
        document.getElementsByClassName("number-button")[i].id = 'inactive-number-button';
    }
}

function getSelectedFieldElement(){
    for (let i = 0; i < 81; i++){
        let field = document.getElementsByClassName('board-tile')[i]
        if ((field.dataset.tilerow === selected_field_index[0]) && (field.dataset.tilecol === selected_field_index[1])){
            return field
        }
    }
}

function getFieldElementByRowCol(row, col){
    for (let i = 0; i < 81; i++){
        let field = document.getElementsByClassName('board-tile')[i]
        if ((field.dataset.tilerow === row.toString()) && (field.dataset.tilecol === col.toString())){
            return field
        }
    }
}

function markFieldWithPen(number, tile){
    tile.innerHTML = number
    game_data['game_state'][parseInt(selected_field_index[0])][parseInt(selected_field_index[1])] = number
    game_data['pencil_markups'][parseInt(selected_field_index[0])][parseInt(selected_field_index[1])] = []
    unmarkFieldMistake(tile)
    requestUpdateGameState(selected_field_index)
}

function markFieldWithPencil(number ,tile, update){
    let selected_row = parseInt(tile.dataset.tilerow);
    let selected_col = parseInt(tile.dataset.tilecol);
    let field_markups = game_data['pencil_markups'][selected_row][selected_col]
    game_data['game_state'][selected_row][selected_col] = 0
    if (tile.firstElementChild !== null){
        if (parseInt(tile.firstElementChild.children[number-1].innerHTML) !== number) {
            tile.firstElementChild.children[number - 1].innerHTML = number;
            if (!field_markups.includes(number)) {
                field_markups.push(number)
            }
        } else {
            tile.firstElementChild.children[number - 1].innerHTML = null;
            let index = field_markups.indexOf(number);
            field_markups.splice(index, 1);
        }
    } else {
        tile.innerHTML = '<div class="parent-pencil-tile" data-tilerow="{{ 3*i+x }}" data-tilecol="{{ 3*j+y }}"></div>';
        let innerDivHTML = "";
        for (let i = 0; i < 9; i++){
            if (number === i+1){
                innerDivHTML += '<div class="pencil-tile" id="'+(i+1)+'" data-tilerow="{{ 3*i+x }}" data-tilecol="{{ 3*j+y }}">'+number+'</div>';
                if (!field_markups.includes(number)) {
                    field_markups.push(number)
                }
            } else {
                innerDivHTML += '<div class="pencil-tile" id="'+(i+1)+'" data-tilerow="{{ 3*i+x }}" data-tilecol="{{ 3*j+y }}"></div>';
            }
        }
        tile.firstElementChild.innerHTML = innerDivHTML;
    }
    if (update === true){
        unmarkFieldMistake(tile)
        requestUpdateGameState(selected_field_index)
    }
}

function eraseField(tile){
    tile.innerHTML = ""
    let selected_row = tile.dataset.tilerow;
    let selected_col = tile.dataset.tilecol;
    game_data['game_state'][parseInt(selected_row)][parseInt(selected_col)] = 0;
    game_data['pencil_markups'][selected_row][selected_col] = [];
    unmarkFieldMistake(tile);
    requestUpdateGameState(selected_field_index);
}

function unmarkFieldMistake(tile){
    if (((selected_number !== null) && (selected_tool === 1)) || (selected_tool === 2)){
        if ((tile.id !== 'selected-tile') && (tile.id !== 'mistake-tile')) {
            tile.id = '';
        } else {
            tile.id = 'selected-tile';
        }
    } else {
        tile.id = 'selected-tile';
    }
}

function requestUpdateGameState(field_index) {
    fetch('/game/update_game_state', {
        method: 'POST',
        body: JSON.stringify({
            'pencil_markups': JSON.stringify(game_data['pencil_markups']),
            'game_state': JSON.stringify(game_data['game_state']),
            'field_index': JSON.stringify([parseInt(field_index[0]), parseInt(field_index[1])])
        }),
        headers: {'Content-Type': 'application/json'}
    }).then(function (response) {
        response.json().then(function (json) {
            if (json['won']){
                deselectAllFields();
                removeAllEventListeners();
                deactivateNumberButtons();
                clearInterval(timerInterval);
                let boardTitleElement = document.getElementsByClassName('board-title')[0];
                boardTitleElement.id = 'solved-board-title';
                boardTitleElement.innerHTML = 'SOLVED ' + boardTitleElement.innerHTML;
                document.getElementById('back-button').firstElementChild.setAttribute('href','/');
                document.getElementById('back-button').firstElementChild.firstElementChild.innerHTML = 'BACK TO MENU';

            } else {
                document.getElementsByClassName('mistakes-counter')[0].innerHTML = json['mistakes'];
                game_data['mistake_fields'] = json['mistake_fields'];
                markMistake(field_index);
            }
            getFoundNumbers();
            deactivateFoundNumberButtons();
        });
    })
}

function Timer() {
    game_data['elapsed_time'] += 1;
    document.getElementsByClassName('timer-counter')[0].innerText = timeFormat(game_data['elapsed_time']);
}

function timeFormat(elapsedT) {
    const {hours, minutes, seconds} = timeBits(elapsedT);
    return hoursFormat(hours) + padString(minutes) + ":" + padString(seconds);
}

function hoursFormat(hours) {
    if (hours > 0) {
        return hours + 'h ';
    }
    return '';
}

function timeBits(timestamp) {
    const hours = Math.floor(timestamp / 3600);
    const minutes = Math.floor((timestamp - (hours * 3600)) / 60);
    const seconds = timestamp - (hours * 3600) - (minutes * 60);
    return {hours, minutes, seconds};
}

function padString(time) {
    const stringTime = time.toString();
    if (stringTime.length === 1) {
        return '0' + stringTime;
    }
    return stringTime;
}

function populateMarkups(){
    for (let i = 0; i < 9; i++){
        for (let j = 0; j < 9; j++){
            for (let k = 0; k < game_data['pencil_markups'][i][j].length; k++){
                let number = game_data['pencil_markups'][i][j][k];
                let tile = getFieldElementByRowCol(i, j);
                markFieldWithPencil(number, tile, false);
            }
        }
    }
}

function markMistake(field_index) {
    for (let k = 0; k < game_data['mistake_fields'].length; k++) {
        let mistake_tile = getFieldElementByRowCol(game_data['mistake_fields'][k][0], game_data['mistake_fields'][k][1]);
        let mistake_tile_row = game_data['mistake_fields'][k][0];
        let mistake_tile_col = game_data['mistake_fields'][k][1];
        if ((mistake_tile_row === parseInt(field_index[0])) && (mistake_tile_col === parseInt(field_index[1]))){
            mistake_tile.id = 'mistake-tile';
        }
    }
}

function populateMistakes() {
    for (let k = 0; k < game_data['mistake_fields'].length; k++) {
        let mistake_tile = getFieldElementByRowCol(game_data['mistake_fields'][k][0], game_data['mistake_fields'][k][1]);
        mistake_tile.id = 'mistake-tile';
    }
}

function getFoundNumbers(){
    found_numbers = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for (let x = 0; x < 9; x++){
        for (let y = 0; y < 9; y++) {
            if (game_data['game_state'][x][y] !== 0) {
                let mistake = false;
                for(let k = 0; k < game_data['mistake_fields'].length; k++){
                    if(game_data['mistake_fields'][k][0] === x && game_data['mistake_fields'][k][1] === y){
                        mistake = true;
                    }
                }
                if (!mistake){
                    found_numbers[(game_data['game_state'][x][y]).toString()] += 1;
                }
            }
        }
    }
}

function deactivateFoundNumberButtons() {
    for (let p = 1; p < 10; p++) {
        let numberButton = document.getElementsByClassName('number-button')[p - 1]
        if (found_numbers[p] === 9) {
            numberButton.id = 'inactive-number-button';
            if (selected_number === p.toString()) {
                selected_number = null;
            }
        } else {
            if ((numberButton.id === 'inactive-number-button') && (selected_tool !== 2)) {
                numberButton.id = 'hoverable-number-button';
            }
        }
    }
}

addToolButtonsEventListeners();
addNumberButtonsEventListeners();
addBoardFieldEventListeners();
addKeyboardEventListeners();
Timer();
populateMarkups();
populateMistakes();
getFoundNumbers();
deactivateFoundNumberButtons();