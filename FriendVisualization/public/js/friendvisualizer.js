var setOfVisitedNodes = [];
$(document).ready(function() {
  $.getJSON('/addNewFriend/0', function (json) {
      setOfVisitedNodes.push(json.id);
      setOfVisitedNodes.push(json.children[0].id);
      console.log(json)
      var infovis = document.getElementById('infovis');
      var w = infovis.offsetWidth - 50, h = infovis.offsetHeight - 50;

      //init Hypertree
      var ht = new $jit.Hypertree({
        //id of the visualization container
        injectInto: 'infovis',
        //canvas width and height
        width: w,
        height: h,
        //Change node and edge styles such as
        //color, width and dimensions.
        Node: {
            //overridable: true,
            'transform': false,
            color: "#ff0000"
        },

        Edge: {
            overridable: true,
            //color: "#ffff00"
        },

        //calculate nodes offset
        offset: 0.2,
        //Change the animation transition type
        transition: $jit.Trans.Back.easeOut,
        //animation duration (in milliseconds)
        duration:1000,
        //Attach event handlers and add text to the
        //labels. This method is only triggered on label
        //creation

        onCreateLabel: function(domElement, node){
          //console.log(domElement);
            domElement.innerHTML = node.name;
            domElement.style.cursor = "pointer";
            domElement.onclick = function() {
              $.getJSON('/addNewFriend', function(json) {
                  ht.op.sum(json, {
                      type: "fade:seq",
                      fps: 30,
                      duration: 1000,
                      hideLabels: false,
                      onComplete: function(){
                          console.log("New nodes added!");
                      }
                  });
              });
            }
        },
        //Change node styles when labels are placed
        //or moved.
        onPlaceLabel: function(domElement, node){
                var width = domElement.offsetWidth;
                var intX = parseInt(domElement.style.left);
                intX -= width / 2;
                //console.log(domElement);
                domElement.style.left = intX + 'px';
        },
        onBeforePlotLine(adj) {
          //console.log(adj);
          //console.log(adj);
          var nodeColor = adj.nodeFrom.data.color
          console.log(nodeColor)
            if(nodeColor === "True") {
              adj.Edge.color = "#ffff00" ;
            }
            else   {
              adj.Edge.color = "#13BBBB";
            }


        },

        onComplete: function(){
          addNodes();
        }
      });
      var count = 0;
      var addNodes = function() {
        count++;
        $.getJSON('/addNewFriend/'+count, function(json) {
          console.log(json);
            ht.op.sum(json, {
                type: "fade:seq",
                fps: 30,
                duration: 0.1,
                hideLabels: false,
                onComplete: function(){

                    //console.log('infi');
                    console.log(count);
                    if (count < 1000) {
                      addNodes();
                    }

                }
            });
        });
      }
      //load JSON data.
      ht.loadJSON(json);
      //compute positions and plot.
      ht.refresh();
      //end
      ht.controller.onBeforeCompute(ht.graph.getNode(ht.root));
      ht.controller.onAfterCompute();
      ht.controller.onComplete();

    });



});
