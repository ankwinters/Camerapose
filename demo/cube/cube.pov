 #version 3.7;
//Includes a separate file defining a number of common colours
 #include "colors.inc"
 #include "textures.inc"
 global_settings { assumed_gamma 1.0 }

//Sets a background colour for the image (dark grey)
 background   { color rgb <0.25, 0.25, 0.25> }

//Places a camera
//direction : Sets, among other things, the field of view of the camera
//right: Sets the aspect ratio of the image
//look_at: Tells the camera where to look
 camera       { 
	            location  <0.0, 0.0, -2.0>
                direction 0.002*z
                up   0.003*y
                right     0.003*x*image_width/image_height
                //angle   67.38
                look_at   <0.0, 0.0, 0.0> }

//Places a light source
//color : Sets the color of the light source (white)
//translate : Moves the light source to a desired location
 light_source { <0, 0, 0>
                color rgb <1, 1, 1>
                translate <-5, 5, -5> }
//Places another light source
//color : Sets the color of the light source (dark grey)
//translate : Moves the light source to a desired location
 light_source { <0, 0, 0>
                color rgb <0.25, 0.25, 0.25>
                translate <6, -6, -6> }

//Sets a box
//pigment : Sets a color for the box ("Red" as defined in "colors.inc")
//finish  : Sets how the surface of the box reflects light
//normal  : Sets a bumpiness for the box using the "agate" in-built model
//rotate : Rotates the box
 box          { //<-0.5, -0.5, -0.5>,
                //<0.5, 0.5, 0.5>
	            0,1
                texture {Gold_Metal 
					     //pigment { checker color Red }
                          finish  { specular 0.6 }
                          normal  { agate 0.25 scale 1/2 }
						  //normal { 0.25 scale 1/2 }
                        }
                rotate <45,46,47> }
//Sets a cylinder dock circle
 cylinder { <0., 0, -0.5>,
	        <0., 0, -0.55>,
			0.2
			texture{ pigment {color Black}
			}
			rotate <45,46,47>
		}

//}
