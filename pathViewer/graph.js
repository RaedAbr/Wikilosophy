var edges = new Map()

String.prototype.hashCode = function() {
    var hash = 0, i, chr;
    if (this.length === 0) return hash;
    for (i = 0; i < this.length; i++) {
      chr   = this.charCodeAt(i);
      hash  = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
  };

//load data into map
d3.tsv("./output.csv", function(error, rows) {
    rows.forEach(function(d){
      edges.set(d.from.toLowerCase(), d.to.toLowerCase());
    });
    
    var next = prompt("Please enter a start page!", "Hello");
    next = next.toLowerCase();
    var path = [];
    var options = {};
    var graphPath = new vis.DataSet(options);
    var graphEdges = new vis.DataSet(options);

    while(!path.includes(next)){
        path.push(next);
        var id = next.hashCode()
        graphPath.add({id: id, label: next, color: next == "philosophy" ? "red" : "cyan"});
        if(path.length > 1){
            graphEdges.add({from: path[path.length - 2].hashCode(), to: id})
        }
        var next2 = edges.get(next);
        if(next2 != null){
            next = next2
        }
    }

    console.log(path);

  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: graphPath,
    edges: graphEdges
  };
  var network = new vis.Network(container, data, options);

});