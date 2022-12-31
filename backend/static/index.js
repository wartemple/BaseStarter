document.write(`<html>
<body>
  <div class="grid-container">
	<div id="grid-item1" style="width: 600px;height:400px;">1</div>
	<div id="grid-item2" style="width: 600px;height:400px;">1</div>
  </div>
  <script type="text/javascript">
	var myChart = echarts.init(document.getElementById('grid-item1'));
	var option = {
	  title: {
		text: "{{option.title.text}}"
	  },
	  tooltip: {},
	  legend: {
		data: ['销量']
	  },
	  xAxis: {
		data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
	  },
	  yAxis: {},
	  series: [
		{
		  name: '销量',
		  type: 'bar',
		  data: [5, 20, 36, 10, 10, 20]
		}
	  ]
	}
	myChart.setOption(option);

	var myChart = echarts.init(document.getElementById('grid-item2'));
	var option = {
	  title: {
		text: "{{option.title.text}}"
	  },
	  tooltip: {},
	  legend: {
		data: ['销量']
	  },
	  xAxis: {
		data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
	  },
	  yAxis: {},
	  series: [
		{
		  name: '销量',
		  type: 'bar',
		  data: [5, 20, 36, 10, 10, 20]
		}
	  ]
	}
	myChart.setOption(option);
  </script>
</body>
</html>`)