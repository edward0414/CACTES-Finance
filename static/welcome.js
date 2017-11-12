$(function(){
        updateBalance();
    
        
        //------- Filter feature ------------------------

        $("#filterType").on("change", function() {
        //filter by type
            
            var type;
            if ($(this).val() == "All") {
                type = "";
            } else {
                type = $(this).val().toLowerCase();
            }
            
            var month;
            month = $("#filterMonth").val();
            if (!month || month == "All") {
                month = "";
            } else {
                month = month.toLowerCase();
                if (month == "january") {
                    month="01";
                } else if (month == "february") {
                    month="02";
                } else if (month == "march") {
                    month="03";
                } else if (month == "april") {
                    month="04";
                } else if (month == "may") {
                    month="05";
                } else if (month == "june") {
                    month="06";
                } else if (month == "july") {
                    month="07";
                } else if (month == "august") {
                    month="08";
                } else if (month == "september") {
                    month="09";
                } else if (month == "october") {
                    month="10";
                } else if (month == "november") {
                    month="11";
                } else if (month == "december") {
                    month="12";
                }
            }
            
            var year;
            year = $("#filterYear").val();
            if (!year || year == "All") {
                year = "";
            } else {
                year = year.toLowerCase();
            }
            
            
            $("#transactions tr").each(function() {
              var result = ($(this).find('.date').text().indexOf(month) == 5 || $(this).find('.date').text().indexOf(month) == 0);
                // filter month
                
                result = result && $(this).text().toLowerCase().indexOf(type) > -1;
                // filter type
                
                result = result && $(this).text().toLowerCase().indexOf(year) > -1;
                // filter year
                
                $(this).toggle(result)
            });
            updateBalance();
        });
    
    
    
    
        $("#filterYear").on("change", function() {
        //filter by year
            
            var year;
            if ($(this).val() == "All") {
                year = "";
            } else {
                year = $(this).val().toLowerCase();
            }
            
            var type;
            type = $("#filterType").val();
            if (!type || type == "All") {
                type = "";
            } else {
                type = type.toLowerCase();
            }
            
            var month;
            month = $("#filterMonth").val();
            if (!month || month == "All") {
                month = "";
            } else {
                month = month.toLowerCase();
                if (month == "january") {
                    month="01";
                } else if (month == "february") {
                    month="02";
                } else if (month == "march") {
                    month="03";
                } else if (month == "april") {
                    month="04";
                } else if (month == "may") {
                    month="05";
                } else if (month == "june") {
                    month="06";
                } else if (month == "july") {
                    month="07";
                } else if (month == "august") {
                    month="08";
                } else if (month == "september") {
                    month="09";
                } else if (month == "october") {
                    month="10";
                } else if (month == "november") {
                    month="11";
                } else if (month == "december") {
                    month="12";
                }
            }
            
            $("#transactions tr").each(function() {
              var result = ($(this).find('.date').text().indexOf(month) == 5 || $(this).find('.date').text().indexOf(month) == 0);
                // filter month
                
                result = result && $(this).text().toLowerCase().indexOf(type) > -1;
                // filter type
                
                result = result && $(this).text().toLowerCase().indexOf(year) > -1;
                // filter year
                
                $(this).toggle(result)
            });
            updateBalance();
        });
    
    
    
    
        $("#filterMonth").on("change", function() {
        //filter by month
            
            var month;
            if ($(this).val() == "All") {
                month = "";
            } else {
                month = $(this).val().toLowerCase();
                if (month == "january") {
                    month="01";
                } else if (month == "february") {
                    month="02";
                } else if (month == "march") {
                    month="03";
                } else if (month == "april") {
                    month="04";
                } else if (month == "may") {
                    month="05";
                } else if (month == "june") {
                    month="06";
                } else if (month == "july") {
                    month="07";
                } else if (month == "august") {
                    month="08";
                } else if (month == "september") {
                    month="09";
                } else if (month == "october") {
                    month="10";
                } else if (month == "november") {
                    month="11";
                } else if (month == "december") {
                    month="12";
                }
            }
            
            var type;
            type = $("#filterType").val();
            if (!type || type == "All") {
                type = "";
            } else {
                type = type.toLowerCase();
            }
            
            var year;
            year = $("#filterYear").val();
            if (!year || year == "All") {
                year = "";
            } else {
                year = year.toLowerCase();
            }
            
            $("#transactions tr").each(function() {
                var result = ($(this).find('.date').text().indexOf(month) == 5 || $(this).find('.date').text().indexOf(month) == 0);
                // filter month
                
                result = result && $(this).text().toLowerCase().indexOf(type) > -1;
                // filter type
                
                result = result && $(this).text().toLowerCase().indexOf(year) > -1;
                // filter year
                
                $(this).toggle(result)
            });
            updateBalance();
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
            
            
            var query = "/transactions/" + id;
            
            
            //------ moneyCount and Cheques part ----------
            
            $.getJSON(query, function(data){
            //send a GET request to get the moneyCount and cheque data
                
                
                
                var editComment = "(Last edit: " + data.transaction.lastEdit + " on " + data.transaction.lastEditTime + ")";
                    
                $('#edit').html(editComment);

                
                
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
                        contents += buildCheque(i+1, data.cheques[i].chequeType, data.cheques[i].chequeNum, data.cheques[i].issuedBy, data.cheques[i].payTo, data.cheques[i].amount);
                        $('#cheques').html(contents);
                    }
                    
                } else {
                    $('#cheques').html('<label class="data-result" style="padding-left:7.5%;">There is no cheque involved in this transaction.</label><br>');
                }
            });
            
            $("#modify").on('click', function(){
                console.log(id);
                location.href='/modifyTransaction/' + id;
            });
            
        });

});






function updateBalance() {
    //helper function for updating the balance for the rows on the table
    
    var l= document.getElementById("total").rows.length -4;
    var i;
    var itotal=0;
    var etotal=0;
    for (i=1;i<l+1;i++) {
        if (document.getElementById("total").rows[i].style.display != "none") {
            itotal += parseFloat(document.getElementById("total").rows[i].cells[6].innerHTML, 10);
            etotal += parseFloat(document.getElementById("total").rows[i].cells[7].innerHTML, 10);
        }
    }
    itotal = itotal.toFixed(2);
    etotal = etotal.toFixed(2);
    b = itotal-etotal;
    b = b.toFixed(2);
    document.getElementById("iTotal").innerHTML = "$ " + itotal;
    document.getElementById("eTotal").innerHTML = "$ " + etotal;
    document.getElementById("balance").innerHTML = "$ " + b;
    
    if (itotal-etotal <0) {
        $("#balance").css("backgroundColor", "#d9534f");
        $("#balance").css("color","#f9f9f9");
        $('#balanceComment').html("Warning:");
        $('#balanceComment').css("color", "#d9534f");
    } else {
        $("#balance").css("backgroundColor", "#5cb85c");
        $("#balance").css("color","#f9f9f9");
        $('#balanceComment').html("Healthy:");
        $('#balanceComment').css("color", "#5cb85c");
    }
    
    
    var ratio;
    if (itotal == 0) {
        $("#ratio").html("Invalid ratio: No income.");
        $("#ratio").css("backgroundColor", "#ffbb33");
        $("#ratio").css("color","#f9f9f9");
        $('#ratioComment').html("Warning:");
        $('#ratioComment').css("color", "#ffbb33");
    } else {
        ratio = (etotal / itotal * 100).toFixed(2);
        document.getElementById("ratio").innerHTML = (ratio) + "%";
        
        if (ratio >= 100) {
            $("#ratio").css("backgroundColor", "#d9534f");
            $("#ratio").css("color","#f9f9f9");
            $('#ratioComment').html("Warning:");
            $('#ratioComment').css("color", "#d9534f");
        } else {
            $("#ratio").css("backgroundColor", "#5cb85c");
            $("#ratio").css("color","#f9f9f9");
            $('#ratioComment').html("Healthy:");
            $('#ratioComment').css("color", "#5cb85c");
        }
    }
}




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


function buildCheque(num, type, cheqNum, issued, paid, amount) {
//helper function that builds the html box
    
    var result = '<div style="padding:0 4%;"><table class="table table-bordered table-hover"><tr><td class="heading" colspan="4" style="font-size:20px;font-weight:bold;">Cheque '+num+'</td></tr><tr><td style="font-size:20px;font-weight:bold;">Type</td><td class="data-result">'+type+'</td><td style="font-size:20px;font-weight:bold;">Issued By</td><td class="data-result">'+issued+'</td></tr><tr><td style="font-size:20px;font-weight:bold;">Cheque #</td><td class="data-result">'+cheqNum+'</td><td style="font-size:20px;font-weight:bold;">Pay To</td><td class="data-result">'+paid+'</td></tr><tr><td colspan="1" style="font-size:20px;font-weight:bold;">Amount</td><td colspan="3" class="data-result">'+' $ '+amount+'</td></tr></table></div><br>';
    return result;
}


var _headers = [{ idx: 0, key: 'ID', type: 'number', display: 'ID'},
				{ idx: 1, key: 'type', type: 'text', display: 'Type'},
				{ idx: 2, key: 'date', type: 'text', display: 'Date'},
				{ idx: 3, key: 'person', type: 'text', display: 'Person Responsible'},
				{ idx: 4, key: 'approved', type: 'text', display: 'Approved By'},
               { idx: 5, key: 'event', type: 'text', display: 'Event'},
               { idx: 6, key: 'income', type: 'number', display: 'Income' },
               { idx: 7, key: 'expense', type: 'number', display: 'Expense' }];


var sort = function (elm) {
	if ($(elm).length) {
		var _key = elm.dataset.key;
		var _header = _.find(_headers, function (h, i) { return h.key == _key; });

		var _idx = _header.idx;
		var _type = _header.type;

		if (_.include(['text', 'number'], _type)) {
			$('.table .glyphicon').hide();

			var _table = $('#total');
			var _dir = 'asc';
			var _switching = true;
			var _rows, _i, _x, _y, _s, _c = 0;

		  	while (_switching) {
			    _switching = false;
			    _rows = _table.find('tbody tr');

			    for (_i = 0; _i < (_rows.length - 1); _i ++) {
				    _s = false;
				    
				    _x = _rows[_i].getElementsByTagName('td')[_idx];
				    _y = _rows[_i + 1].getElementsByTagName('td')[_idx];
				      	
				    if (_type == 'text') {
				    	_v1 = _x.innerHTML.toLowerCase();
				    	_v2 = _y.innerHTML.toLowerCase();
				    }
				    else if (_type == 'number') {
				    	_v1 = parseFloat(_x.innerHTML);
				    	_v2 = parseFloat(_y.innerHTML);
				    }

				    if (_dir == 'asc') {
					    if (_v1 > _v2) {
					   		_s= true;
				       		break;
			       		}
			       	}
					else if (_dir == 'desc') {
				   		if (_v1 < _v2) {
			       			_s= true;
			       			break;
			      		}
					}
				}
				    
				if (_s) {
				  	_rows[_i].parentNode.insertBefore(_rows[_i + 1], _rows[_i]);
			     	_switching = true;

				   	_c ++;      
				} 
			    else {
			      	if (_c == 0 && _dir == 'asc') {
					    _dir = 'desc';
				    	_switching = true;
			      	}
				}
			}

			if (_dir == 'asc') {
				_table.find('thead th:nth-of-type(' + (_idx + 1) + ') .glyphicon-triangle-top').show();
			}
			else if (_dir == 'desc') {
				_table.find('thead th:nth-of-type(' + (_idx + 1) + ') .glyphicon-triangle-bottom').show();
			}
		}
	}
}

