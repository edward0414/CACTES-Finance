$(function(){
    
        $("#numCheques").on('click', function() {
            addFields();
        });

});


//Sample Cheque Form
/*
<div style="padding-left:7.5%;">
<h3 class="custom-label">Cheque 1</h3>
    <div class="form-one-line">
        <div style="display:flex; flex-direction:column; padding-right:5%">
            <div class="form-one-line">
                <label style="font-size:15px; padding-right:107px">Type</label>
                <select type="number" name="chequeType" class="form-control" style="width:75px;" required autofocus>
                    <option>Income</option>
                    <option>Expense</option>
                </select>
            </div>
            <div class="form-one-line">
                <label style="font-size:15px; padding-right:24px">Cheque Number</label>
                <input type="number" name="chequeNum" class="form-control" style="width:75px;" required>
            </div>
        </div>
        <div class="form-one-column">
            <div class="form-one-line">
                <label style="font-size:15px; padding-right:35px">Issued By</label>
                <input type="text" name="issuedBy" class="form-control" style="width:60%;" required>
            </div>
            <div class="form-one-line">
                <label style="font-size:15px; padding-right:57px">Pay To</label>
                <input type="text" name="payTo" class="form-control" style="width:60%;" required>
            </div>
        </div>
    </div>
    <div class="form-one-line">
        <label style="font-size:15px; padding-right:35px">Cheque Amount</label>
        <input type="number" step="0.01" min="0" name="chequeAmount" class="form-control" style="width:60%;" required>
    </div>
</div>
<br>
*/


function buildCheque(num) {
//function that builds the html box
//enter string name, string content, int num
    var result = '<div style="padding-left:7.5%;"><h3 class="custom-label">Cheque '+num+'</h3><div class="form-one-line"><div style="display:flex; flex-direction:column; padding-right:5%"><div class="form-one-line"><label style="font-size:15px; padding-right:107px">Type</label><select type="number" name="chequeType" class="form-control" style="width:75px;" required autofocus><option>Income</option><option>Expense</option></select></div><div class="form-one-line"><label style="font-size:15px; padding-right:24px">Cheque Number</label><input type="number" name="chequeNum" class="form-control" style="width:75px;" required></div></div><div class="form-one-column"><div class="form-one-line"><label style="font-size:15px; padding-right:35px">Issued By</label><input type="text" name="issuedBy" class="form-control" style="width:60%;" required></div><div class="form-one-line"><label style="font-size:15px; padding-right:57px">Pay To</label><input type="text" name="payTo" class="form-control" style="width:60%;" required></div></div></div><div class="form-one-line"><label style="font-size:15px; padding-right:35px">Cheque Amount</label><input type="number" step="0.01" min="0" name="chequeAmount" class="form-control" style="width:60%;" required></div></div><br>';
    return result;
}


function addFields(){
    document.getElementById("cheque").innerHTML = "";
    var number = document.getElementById("numCheques").value;
    for (i=0;i<number;i++){
        var contents = document.getElementById("cheque").innerHTML;
        contents += buildCheque(i+1);
        document.getElementById("cheque").innerHTML = contents;
        console.log("Completed " + i);
    }
}