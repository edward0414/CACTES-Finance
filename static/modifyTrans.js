$(function(){
    
        $("#numCheques").on('click', function() {
            addFields();
        });
    
        // ----- Modal Feature ---------------------
    
    
        $(".table").find('tr[data-target]').on('click', function(){
            
            
            //------ basic transaction info ------------
            
            var id = $(this).find('.id').html()
            $('#transID').html(id);
            
            var type = $(this).find('.type').html()
            $('#type').html(type);
            
            var date = $(this).find('.date').html()
            $('#date').html(date);
            
            var person = $(this).find('.staff').html()
            $('#staff').html(person);
            
            var approved = $(this).find('.approved').html()
            $('#approvedBy').html(approved);
            
            var event = $(this).find('.event').html()
            $('#event').html(event);
            
            var income = $(this).find('.income').html()
            $('#income').text(' $ '+income);
            
            var expense = $(this).find('.expense').html()
            $('#expense').text(' $ '+expense);
            
            var query = "http://localhost:4000/transactions/" + id
            
            
            //------ moneyCount and Cheques part ----------
            
            $.getJSON(query, function(data){
            //send a GET request to get the moneyCount and cheque data
                
                for (var i=0;i<data.moneyCounts.length;i++) {
                    //------ handling moneyCount -------
                    
                    if (data.moneyCounts[i].moneyType == "Income") {
                        $('#i-bill5').html(data.moneyCounts[i].num5bill);
                        $('#i-bill10').html(data.moneyCounts[i].num10bill);
                        $('#i-bill20').html(data.moneyCounts[i].num20bill);
                        $('#i-bill50').html(data.moneyCounts[i].num50bill);
                        $('#i-bill100').html(data.moneyCounts[i].num100bill);
                        $('#i-nickel').html(data.moneyCounts[i].numNickel);
                        $('#i-dime').html(data.moneyCounts[i].numDime);
                        $('#i-quarter').html(data.moneyCounts[i].numQuarter);
                        $('#i-loonie').html(data.moneyCounts[i].numLoonie);
                        $('#i-toonie').html(data.moneyCounts[i].numToonie);
                        
                    } else if (data.moneyCounts[i].moneyType == "Expense") {
                        $('#e-bill5').html(data.moneyCounts[i].num5bill);
                        $('#e-bill10').html(data.moneyCounts[i].num10bill);
                        $('#e-bill20').html(data.moneyCounts[i].num20bill);
                        $('#e-bill50').html(data.moneyCounts[i].num50bill);
                        $('#e-bill100').html(data.moneyCounts[i].num100bill);
                        $('#e-nickel').html(data.moneyCounts[i].numNickel);
                        $('#e-dime').html(data.moneyCounts[i].numDime);
                        $('#e-quarter').html(data.moneyCounts[i].numQuarter);
                        $('#e-loonie').html(data.moneyCounts[i].numLoonie);
                        $('#e-toonie').html(data.moneyCounts[i].numToonie);
                    }
                }
                
                //------ handling cheque part -----
                if (data.cheques.length != 0 ) {
                    $('#cheques').html("");
                    for (var i=0; i<data.cheques.length; i++) {
                        var contents = $('#cheques').html();
                        contents += buildCheques(i+1, data.cheques[i].chequeType, data.cheques[i].chequeNum, data.cheques[i].issuedBy, data.cheques[i].payTo, data.cheques[i].amount);
                        $('#cheques').html(contents);
                    }
                    
                } else {
                    console.log("no cheque!");
                    $('#cheques').html('<label class="data-result" style="padding-left:7.5%;">There is no cheque involved in this transaction.</label><br>');
                }
            });
        });

});




//Sample Cheque Result
/*
<br>
<div style="padding:0 3.5%;">
<table class="table table-bordered table-hover">
    <tr>
        <td colspan="4" style="font-size:20px;font-weight:bold;">Cheque</td>
    </tr>
    <tr>
        <td style="font-size:20px;font-weight:bold;">Type</td>
        <td class="data-result"></td>
        <td style="font-size:20px;font-weight:bold;">Issued By</td>
        <td class="data-result"></td>
    </tr>
    <tr>
        <td style="font-size:20px;font-weight:bold;">Cheque Number</td>
        <td class="data-result"></td>
        <td style="font-size:20px;font-weight:bold;">Pay To</td>
        <td class="data-result"></td>
    </tr>
    <tr>
        <td colspan="2" style="font-size:20px;font-weight:bold;">Cheque Amount</td>
        <td colspan="2" class="data-result"></td>
    </tr>
</table>
</div>
<br>
*/


function buildCheques(num, type, cheqNum, issued, paid, amount) {
//helper function that builds the html box
    
    var result = '<br><div style="padding:0 4%;"><table class="table table-bordered table-hover"><tr><td class="heading" colspan="4" style="font-size:20px;font-weight:bold;">Cheque '+num+'</td></tr><tr><td style="font-size:20px;font-weight:bold;">Type</td><td class="data-result">'+type+'</td><td style="font-size:20px;font-weight:bold;">Issued By</td><td class="data-result">'+issued+'</td></tr><tr><td style="font-size:20px;font-weight:bold;">Cheque #</td><td class="data-result">'+cheqNum+'</td><td style="font-size:20px;font-weight:bold;">Pay To</td><td class="data-result">'+paid+'</td></tr><tr><td colspan="1" style="font-size:20px;font-weight:bold;">Amount</td><td colspan="3" class="data-result">'+' $ '+amount+'</td></tr></table></div><br>';
    return result;
}



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
        <input type="number" name="chequeAmount" class="form-control" style="width:60%;" required>
    </div>
</div>
<br>
*/


function buildCheque(num) {
//function that builds the html box
//enter string name, string content, int num
    var result = '<div style="padding-left:7.5%;"><h3 class="custom-label">Cheque '+num+'</h3><div class="form-one-line"><div style="display:flex; flex-direction:column; padding-right:5%"><div class="form-one-line"><label style="font-size:15px; padding-right:107px">Type</label><select type="number" name="chequeType" class="form-control" style="width:75px;" required autofocus><option>Income</option><option>Expense</option></select></div><div class="form-one-line"><label style="font-size:15px; padding-right:24px">Cheque Number</label><input type="number" name="chequeNum" class="form-control" style="width:75px;" required></div></div><div class="form-one-column"><div class="form-one-line"><label style="font-size:15px; padding-right:35px">Issued By</label><input type="text" name="issuedBy" class="form-control" style="width:60%;" required></div><div class="form-one-line"><label style="font-size:15px; padding-right:57px">Pay To</label><input type="text" name="payTo" class="form-control" style="width:60%;" required></div></div></div><div class="form-one-line"><label style="font-size:15px; padding-right:35px">Cheque Amount</label><input type="number" name="chequeAmount" class="form-control" style="width:60%;" required></div></div><br>';
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