<html>
<head>
	<title>Balance</title>
	<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
	<link rel="stylesheet" href="style.css">
	<meta http-equiv="refresh" content="300"> <!-- Refresh every 5 minutes -->
</head>
<body>

<?php 
	function LastTotal($f) {
		$lines = file($f);
		$line = end($lines);
		$data = explode(',', $line);
		$total = end($data);
		return $total;
	}

	$dir = '/home/pi/crypto/data/';
	$files = scandir($dir);

	$pos = array_search('TOTAL.txt', $files);
	$tmp = $files[$pos];
	$files[$pos] = $files[0];
	$files[0] = $tmp;

	$pos = array_search('.', $files);
	array_splice($files, $pos, 1);
	$pos = array_search('..', $files);
	array_splice($files, $pos, 1);

	$totals = array();
	$names = array();
	foreach($files as $f) {
		if (pathinfo($f, PATHINFO_EXTENSION) == 'csv') {
			array_push($totals, LastTotal($dir . $f));
			array_push($names, pathinfo($f, PATHINFO_FILENAME));
		}
	}
	$total = array_sum($totals);

	$selected = 'TOTAL.txt';
	if (isset($_POST['submit'])) {
		if (!empty($_POST['submit'])) {
			$selected = $_POST['exchange'];
		}
	}

	$lines = file($dir . $selected);
	$dates = array();
	$balances = array();

	foreach(array_slice($lines, 1) as $line) {
		$data = explode(',', $line);
		array_push( $dates, $data[0] . ' ' . $data[1] );
		array_push( $balances, $data[2] );
	}

#	echo '<p>' . $dates[0] . '</p>';


echo '<h1 style="text-align:center">';
echo number_format((float)$total, 2, '.', '');
echo '</h1>';
?>




<form action="" method="POST">
    <select name="exchange">
        <option selected="selected">Choose an exchange</option>
        <?php
        // Iterating through the product array
        foreach($files as $item){
        	echo "<option value='$item'>$item</option>";
        }
        ?>
    </select>
    <input type="submit" name="submit" value="Submit">
</form>




<div class="float-container">
	<div class="float-child">
	<div id="timeSeries"></div>
	</div>

	<div class="float-child">
	<div id="pie"></div>
	</div>
</div>


<script>
	var total = <?php echo $total; ?>;
	var totals = <?php echo json_encode($totals); ?>;
	var names = <?php echo json_encode($names); ?>;
	var selected = <?php echo json_encode($selected); ?>;
	var naslov = selected.replace(/\.[^/.]+$/, "");

	var dates = <?php echo json_encode($dates); ?>;
	var balances = <?php echo json_encode($balances); ?>;

	PIE = document.getElementById('pie');
	Plotly.newPlot( PIE, [{
		values: totals,
		labels: names,
		type: 'pie'
	 }], { height:400, width: 500 } );

	var rawDataURL = '/home/pi/crypto/data/TOTAL.txt';
	var xField1 = 'Date';
	var xField2 = 'Time';
	var yField = '$';

	var selectorOptions = {
	    buttons: [{
	        step: 'day',
        	stepmode: 'backward',
	        count: 1,
	        label: '1d'
	    }, {
                step: 'day',
                stepmode: 'backward',
                count: 3,
                label: '3d'
            }, {
		step: 'day',
	        stepmode: 'backward',
        	count: 7,
	        label: '1w'
	    }, {
	        step: 'month',
	        stepmode: 'backward',
        	count: 1,
	        label: '1m'
	    }, {
        	step: 'all',
	    }]
	};


/*
#	d3.csv(rawDataURL, function(err, rawData) {
#	    if(err) throw err;
#
#	console.log(rawData);
#
#	    var data = prepData(rawData);
#	    var layout = {
#       	title: 'Time series with range slider and selectors',
#	        xaxis: {
#        	    rangeselector: selectorOptions,
#	            rangeslider: {}
#	        },
#        	yaxis: {
#	            fixedrange: true
#	        }
#	    };
#
#	    Plotly.newPlot('timeSeries', data, layout);
#	});
#
#	function prepData(rawData) {
#	    var x = [];
#	    var y = [];
#
#	    rawData.forEach(function(datum, i) {
#
#	        x.push( new Date( datum[xField1].concat(' ', datum[xField2]) ) );
#	        y.push(datum[yField]);
#	    });
#
#	    return [{
#       	mode: 'lines',
#	        x: x,
#	        y: y
#	    }];
#	}
*/

	TIME = document.getElementById('timeSeries');
	Plotly.newPlot( TIME,
		[{
			x: dates,
			y: balances
		}],
		{
			title: String(naslov),
			xaxis: { rangeselector: selectorOptions },
			yaxis: {}
		} );

</script>



<!-- stops annoying popups on reload -->
<script>
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}
</script>



</body>
</html>
