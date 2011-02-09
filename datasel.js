// code from 
// http://www.adp-gmbh.ch/web/js/hiding_column.html


function show_hide_data(class, do_show) {

    var stl;
    if (do_show) stl = 'block'
    else         stl = 'none';

if (document.getElementsByClassName == undefined) {
	document.getElementsByClassName = function(className)
	{
		var hasClassName = new RegExp("(?:^|\\s)" + className + "(?:$|\\s)");
		var allElements = document.getElementsByTagName("*");
		var results = [];

		var element;
		for (var i = 0; (element = allElements[i]) != null; i++) {
			var elementClass = element.className;
			if (elementClass && elementClass.indexOf(className) != -1 && hasClassName.test(elementClass))
				results.push(element);
		}

		return results;
	}
}



    var elements  = document.getElementsByClassName(class);

    for (var el=0; el<elements.length;el++) {

        elements[el].style.display=stl;
    }

  // set/clear all checkboxes for individual jobs too
  var elements  = document.getElementsByClassName("job_indiv");

  for (var el=0; el<elements.length;el++) {
	
        elements[el].checked=do_show;
  }




}


function show_hide_data_id(id, do_show) {

    var stl;
    if (do_show) stl = 'block'
    else         stl = 'none';




    var element  = document.getElementById(id);

//    alert(elements.length+id);
//    for (var el=0; el<elements.length;el++) {


//        alert("Setting element "+el+" to "+stl);
        element.style.display=stl;
//    }
  }

function toggle_job_blink(owner) {
	//alert("Displaying jobs for "+owner);

  var elements  = document.getElementsByClassName(owner);

  for (var el=0; el<elements.length;el++) {
	alert("x"+elements[el].style.color+"x");
	elements[el].style.textDecoration='blink';
	elements[el].style.backgroundColour='blue';
//	if (elements[el].visibility == '') {
//		elements[el].style.display='none';
//	} else {
//
//	elements[el].style. == 'block'
//	}


  }

}

function highlight(owner) {
	//alert("Displaying jobs for "+owner);

  var elements  = document.getElementsByClassName(owner);

  for (var el=0; el<elements.length;el++) {
//	alert("x"+elements[el].style.color+"x");
	elements[el].style.textDecoration='blink';
	elements[el].style.color='white';
	elements[el].style.backgroundColor='blue';
//	if (elements[el].visibility == '') {
//		elements[el].style.display='none';
//	} else {
//
//	elements[el].style. == 'block'
//	}


  }

}


function dehighlight(owner) {
	//alert("Displaying jobs for "+owner);

  var elements  = document.getElementsByClassName(owner);

  for (var el=0; el<elements.length;el++) {
//	alert("x"+elements[el].style.color+"x");
	elements[el].style.textDecoration='none';
	elements[el].style.backgroundColor='white';
	elements[el].style.color='black';
//	if (elements[el].visibility == '') {
//		elements[el].style.display='none';
//	} else {
//
//	elements[el].style. == 'block'
//	}


  }

}



function on_top(class, on_top) {

    var stl;
    if (on_top) stl = 'fixed'
    else         stl = 'static';

if (document.getElementsByClassName == undefined) {
        document.getElementsByClassName = function(className)
        {
                var hasClassName = new RegExp("(?:^|\\s)" + className + "(?:$|\\s)");
                var allElements = document.getElementsByTagName("*");
                var results = [];

                var element;
                for (var i = 0; (element = allElements[i]) != null; i++) {
                        var elementClass = element.className;
                        if (elementClass && elementClass.indexOf(className) != -1 && hasClassName.test(elementClass))
                                results.push(element);
                }

                return results;
        }
}

    var elements  = document.getElementsByClassName(class);

    for (var el=0; el<elements.length;el++) {

        elements[el].style.position=stl;
    }

}
