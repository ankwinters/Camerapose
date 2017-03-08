# version 3.7;
#include "colors.inc"  
#include "textures.inc"
global_settings { assumed_gamma 1.0 }
//camera       {   
//                location  <0.0, 0.0, -50.0>
//                direction 0.01*z  //焦距为cube_lenmm   
//                up   0.003*y   //相机胶片尺寸为4mm*3mm，像素为800*600
//                right     0.003*x*image_width/image_height
//                
//                look_at   <0.0, 0.0, 0.0> } 

  camera {
    location <-2, -2, 3>
    look_at <0, 0, 0>
  }
  light_source { <50, 50, -50> color rgb<1, 1, 1> }
  light_source { <-50, -50, 50> color rgb<1, 1, 1> }
  #declare Red = texture {
    pigment { color rgb<0.8, 0.2, 0.2> }
    finish { ambient 0.2 diffuse 0.5 }
  }
  #declare Green = texture {
    pigment { color rgb<0.2, 0.8, 0.2> }
    finish { ambient 0.2 diffuse 0.5 }
  }
  #declare Blue = texture {
    pigment { color rgb<0.2, 0.2, 0.8> }
    finish { ambient 0.2 diffuse 0.5 }
  }
  #declare cube_len = 0.5;
mesh {
    /* top side */
    triangle {
      <-cube_len, cube_len, -cube_len>, <cube_len, cube_len, -cube_len>, <cube_len, cube_len, cube_len>
      texture { Red }
    }
    triangle {
      <-cube_len, cube_len, -cube_len>, <-cube_len, cube_len, cube_len>, <cube_len, cube_len, cube_len>
      texture { Red }
    }
    /* bottom side */
	// no color set
    triangle { <-cube_len, -cube_len, -cube_len>, <cube_len, -cube_len, -cube_len>, <cube_len, -cube_len, cube_len> }
    triangle { <-cube_len, -cube_len, -cube_len>, <-cube_len, -cube_len, cube_len>, <cube_len, -cube_len, cube_len> }
    /* left side */
	// no color set
    triangle { <-cube_len, -cube_len, -cube_len>, <-cube_len, -cube_len, cube_len>, <-cube_len, cube_len, cube_len> }
    triangle { <-cube_len, -cube_len, -cube_len>, <-cube_len, cube_len, -cube_len>, <-cube_len, cube_len, cube_len> }
    /* right side */
    triangle {
      <cube_len, -cube_len, -cube_len>, <cube_len, -cube_len, cube_len>, <cube_len, cube_len, cube_len>
      texture { Green }
    }
    triangle {
      <cube_len, -cube_len, -cube_len>, <cube_len, cube_len, -cube_len>, <cube_len, cube_len, cube_len>
      texture { Green }
    }
    /* front side */
    triangle {
      <-cube_len, -cube_len, -cube_len>, <cube_len, -cube_len, -cube_len>, <-cube_len, cube_len, -cube_len>
      texture { Blue }
    }
    triangle {
      <-cube_len, cube_len, -cube_len>, <cube_len, cube_len, -cube_len>, <cube_len, -cube_len, -cube_len>
      texture { Blue }
    }
    /* back side */
    triangle { <-cube_len, -cube_len, cube_len>, <cube_len, -cube_len, cube_len>, <-cube_len, cube_len, cube_len> }
    triangle { <-cube_len, cube_len, cube_len>, <cube_len, cube_len, cube_len>, <cube_len, -cube_len, cube_len> }
    texture {
      pigment { color rgb<0.9, 0.8, 0.8> }
	  finish {specular 0.8 roughness 1}
	  normal { agate 0.25 scale 1/2}
      //finish { ambient 0.2 diffuse 0.7 }
    }
  }
