/*Variable Declarations*/
var province = provinceData;

/*Event Calls*/
$(document).on('change','#id_sk_sorttype', function () {
	startSort(this.value) ;
});


/*init function*/
function init() {
	renderProvinceDropdown();
	registerEvents();
}

function registerEvents() {
}

function renderProvinceDropdown() {
	$('#provinceSelect').empty();
	$('#provinceSelect').append('<option value="None" selected="selected">--Select--</option>');
	$.each(province, function(i, p) {
		$('#provinceSelect').append($('<option></option>').val(p.long_name).html(p.long_name));
	});
}