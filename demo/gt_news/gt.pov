// =========================================
// News vending machine
// -----------------------------------------
// This file contains the following:
// 1. A simple macro that creates US-type news vending machines
// 2. A USA Today vending machine
// -----------------------------------------
// Made for Persistence of vision 3.6
// =========================================  
// Copyright 2000-2004 Gilles Tran http://www.oyonale.com
// -----------------------------------------
// This work is licensed under the Creative Commons Attribution License. 
// To view a copy of this license, visit http://creativecommons.org/licenses/by/2.0/ 
// or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
// You are free:
// - to copy, distribute, display, and perform the work
// - to make derivative works
// - to make commercial use of the work
// Under the following conditions:
// - Attribution. You must give the original author credit.
// - For any reuse or distribution, you must make clear to others the license terms of this work.
// - Any of these conditions can be waived if you get permission from the copyright holder.
// Your fair use and other rights are in no way affected by the above. 
//==========================================  

// -----------------------------------------
// Vending machine macro
// -----------------------------------------
#macro mNewsVM(xVMBox,yVMBox,zVMBox,rtyVMBox,eVM,T_PaintHead,T_PaintBox,T_NewsTop,T_NewsFront,T_NewsBottom,T_LeftSide,T_RightSide,T_BackSide)
// xVMBox, yVMBoxn, ZVMBox = size of the box containing the papers
// rtMBox : ratio between the bottom part of the box (usually with the newspaper name) and the middle part (with the paper of the day)
// eVM : thickness of the box walls
// T_PaintHead : texture of the head (where you put the money)
// T_PaintBox : texture of the box                            
// T_NewsTop : image map for the head (instructions)
// T_NewsFront : image map for the newspaper
// T_NewsBottom : image map for the bottom of the box

// 170308 T_LeftSide:image map for the left side of the box
// T_RightSide:image map for the right side of the box
// T_BackSide: image map for the back of the box

#local xVMHead=xVMBox*0.5;
#local yVMHead=xVMHead/0.7;
#local zVMHead=xVMHead;
#local VMHead=union{
    union{
//                box{0,1 translate -x*0.5 scale <xVMHead/(xVMHead+2*eVM),yVMHead/(yVMHead+eVM),zVMHead/(zVMHead+5*eVM)> translate z*4*eVM} // box
        superellipsoid{<0.1,0.1> scale 0.5 translate <0,0.5,0.5> scale <xVMHead/(xVMHead+2*eVM),yVMHead/(yVMHead+eVM),zVMHead/(zVMHead+5*eVM)> translate z*4*eVM} // box
        cylinder{-0.5*x,x*0.5,1/30 scale <1,1,2> translate <0,29/30,0>}
        union{
            difference{
                box{<-0.5,0,1/3>,<0.5,1,1>}
                plane{z,0 rotate -x*15 translate <0,2/3,1/3>}
                    
            }                        
            difference{
                cylinder{-0.5*x,x*0.5,1/3}
                plane{z,0 inverse}
                plane{y,0 inverse}
                translate <0,1,1/3>
            }
        }
        scale <xVMHead,yVMHead,zVMHead>     
    }                
    box{0,1 texture{T_NewsTop} translate -x*0.5 scale <xVMHead*0.8,yVMHead*0.4,-eVM> translate <0,yVMHead*0.6-eVM*2,1.9*eVM>}
    #declare rC=zVMHead/15;
    difference{
        cone{0,1,x*0.5,0.8}
        cylinder{-x,x*1.1,0.7}
        scale rC
        translate <xVMHead*0.5,rC*3,zVMHead*2/3>
    }
    difference{
        cone{0,1,x*0.5,0.8}
        cylinder{-x,x*1.1,0.7}
        scale rC
        translate <xVMHead*0.5,rC*3,zVMHead*2/3>
        scale <-1,1,1>
    }
    difference{
        cone{0,1,z*0.5,0.8}
        cylinder{-z,z*1.1,0.7}
        scale rC*0.8
        rotate y*180
        translate <0,yVMHead*2/3,eVM>
    }
}                       
#local VMSides=union{
	// 170308 add left texture
	//box{0,<eVM,yVMBox,zVMBox> texture{T_LeftSide} translate <-xVMBox/2,0,0>}  // left
	box{0,<eVM,yVMBox,zVMBox>  translate <-xVMBox/2,0,0>}  // left
	#declare left = box{0,1 texture{T_LeftSide} translate <-0.5,-0.5,0> scale <213,142,1>/213}  // left
    object{left rotate z*45 scale zVMBox/2 rotate y*90 translate <-xVMBox/2-eVM*1.01,yVMBox/2,zVMBox/2>}

	// 170308 add right texture
    box{0,<eVM,yVMBox,zVMBox>  translate <-xVMBox/2,0,0> scale <-1,1,1>} // right
	#declare Right = box{0,1 texture{T_RightSide} translate <0.5,0.5,0> scale <213,142,1>/213}
    object{Right  scale zVMBox/2 rotate -y*90 translate <xVMBox/2+eVM*1.01,yVMBox/2,0>}	
    box{0,1 translate -x*0.5 scale <xVMBox,eVM,zVMBox> translate y*yVMBox} // top
    union{
        union{                // left upper round corner
            difference{cylinder{0,z,1}plane{y,0}plane{x,0 inverse}}
            box{0,1 scale <-1,-3,1>}
            scale <eVM*0.5,eVM,zVMBox>
            translate -x*xVMBox*0.5
        }
        union{                  // right upper round corner
            difference{cylinder{0,z,1}plane{y,0}plane{x,0 inverse}}
            box{0,1 scale <-1,-3,1>}
            scale <eVM*0.5,eVM,zVMBox>
            translate -x*xVMBox*0.5
            scale <-1,1,1>
        }
        translate y*yVMBox     
    }
//*20170308 
// Back side add texture
    box{0,1  translate -x*0.5 scale <xVMBox,yVMBox,eVM> scale <1,1,-1> translate z*(zVMBox-eVM)}
}
#local xVMFront=xVMBox*xVMBox/(xVMBox+3*eVM);
//#warning concat(str(xVMBox+3*eVM,0,3),"\n")
//#warning concat(str(xVMFront,0,3),"\n")
#local yVMFront=rtyVMBox*yVMBox;
#local eVMFront1=xVMBox*0.18/1.4;
#local eVMFront2=eVMFront1*0.4;
#local yVMBottom=yVMBox-yVMFront;
#local VMFront=union{
    // Outer frame
    box{0,1 translate -x*0.5 scale <xVMFront,eVMFront1,eVM>}
    box{0,1 translate -x*0.5 scale <xVMFront,eVMFront1,eVM> scale <1,-1,1> translate y*yVMFront}
    box{0,1 scale <eVMFront1,yVMFront-2*eVMFront1,eVM> translate <-xVMFront*0.5,eVMFront1,0>}
    box{0,1 scale <eVMFront1,yVMFront-2*eVMFront1,eVM> translate <-xVMFront*0.5,eVMFront1,0> scale <-1,1,1>}
    
    // Inner frame
    box{0,1 translate -x*0.5 scale <xVMFront-2*(eVMFront1-eVMFront2),-eVMFront2,-eVM> translate y*eVMFront1}
    box{0,1 translate -x*0.5 scale <xVMFront-2*(eVMFront1-eVMFront2),-eVMFront2,-eVM> scale <1,-1,1> translate y*(yVMFront-eVMFront1)}
    box{0,1 scale <-eVMFront2,yVMFront-2*(eVMFront1-eVMFront2),-eVM> translate <-xVMFront*0.5+eVMFront1,eVMFront1-eVMFront2,0>}
    box{0,1 scale <-eVMFront2,yVMFront-2*(eVMFront1-eVMFront2),-eVM> translate <-xVMFront*0.5+eVMFront1,eVMFront1-eVMFront2,0> scale <-1,1,1>}
    
    // Center pane
    box{0,1 texture{T_NewsFront} translate -x*0.5 scale <xVMFront-2*eVMFront1,yVMFront-2*eVMFront1,eVM> translate y*eVMFront1}
    
    // Hinges
    union{
        cylinder{-x*4/6,-x*2/6,1}
        cylinder{x*2/6,x*4/6,1}
        scale <xVMFront*0.5,2*eVM,2*eVM>
        translate -y*2*eVM
    }
    translate y*yVMBottom
}       
#declare yVMBPane=yVMBottom-2*eVMFront1;
#declare VMBottom=union{
    //Hinges
    union{
        cylinder{-x,-x*0.9*4/6,1}
        cylinder{-x*0.9*2/6,x*0.9*2/6,1}
        cylinder{x,x*0.9*4/6,1}
        scale <xVMFront*0.5,2*eVM,2*eVM>
        translate y*(yVMBottom-2*eVM)
    }    
    cylinder{-x,x,1 scale <xVMFront*0.5,eVMFront1*0.5,eVM> translate y*(yVMBottom-2*eVM-eVMFront1*0.5)}
    // Frame                                                  
    union{
        box{0,1 scale <eVMFront2,yVMBPane,eVM> translate -xVMFront*0.5*x}
        box{0,1 scale <eVMFront2,yVMBPane,eVM> translate -xVMFront*0.5*x scale <-1,1,1>}
        box{0,1 translate -x*0.5 scale <xVMFront,eVMFront2,eVM>}
        box{0,1 translate -x*0.5 scale <xVMFront,eVMFront2,eVM> scale <1,-1,1> translate y*yVMBPane}
        translate y*eVMFront1
    }                
    // Center pane
    box{0,1 texture{T_NewsBottom} translate -x*0.5 scale <xVMFront-2*eVMFront2,yVMBPane-2*eVMFront2,eVM> translate <0,(eVMFront1+eVMFront2),eVM>}
    // Bottom bar
    cylinder{-x,x,1 scale <xVMFront*0.5,eVMFront1*0.5,eVM*2> translate y*eVMFront1*0.5}
    
//        box{0,1 translate -x*0.5 scale <xVMFront,yVMBottom,eVM>}
    
}
#local xVMHandle=xVMHead*2.5/7;
#local yVMHandle=xVMHandle*6/2.5;
#local zVMHandle=6*eVM;
#local rVMHandle=1.5*eVM;
#local rVMHandle2=xVMHandle*0.4;
#local VMHandle=union{
    box{<0,0,-1>,1 translate -x*0.5 scale <xVMHandle,yVMHandle,-zVMHandle>}
    union{                                                    
        cylinder{-x,x,rVMHandle scale <xVMHandle*0.5,1,1> translate y*2*rVMHandle2}
        difference{torus{rVMHandle2,rVMHandle rotate x*90} plane{x,0 inverse} translate <-xVMHandle*0.5,rVMHandle2,0>}
        difference{torus{rVMHandle2,rVMHandle rotate x*90} plane{x,0 inverse} translate <-xVMHandle*0.5,rVMHandle2,0> scale <-1,1,1>}
        rotate -x*75 // you can change the handle angle here
        translate <0,yVMHandle-2*rVMHandle,-zVMHandle*0.5>
    }       
    translate y*(yVMBox-yVMHandle*0.25)
}
#local VMBox=union{
    object{VMSides}
    union{
        object{VMFront}
        object{VMBottom}
        object{VMHandle}
        translate z*eVM*5
    }
}
union{
    object{VMHead texture{T_PaintHead scale yVMHead} translate <0,yVMBox,rVMHandle*2>}
    object{VMBox texture{T_PaintBox scale yVMBox+yVMHandle}}
    
}
#end  

// =========================================
// Examples
// -----------------------------------------

#include "colors.inc"

#declare xVMBox=0.5;
#declare yVMBox=xVMBox*3/1.4;
#declare zVMBox=0.5;
#declare yrtVMBox=0.6;
#declare eVM=0.005;
#declare C_NVM=rgb<1,0.6,0.05>; // yellow
#declare F_Newspaper= finish{ambient 0 diffuse 0.6}
#declare T_NewsTop=texture{pigment{image_map{png "newsmap_2"}} finish{F_Newspaper}}
#declare T_NewsFront=texture{T_NewsTop} // should be different
#declare T_NewsBottom=texture{T_NewsTop} // should be different
#declare N_NVM=normal{bozo 0.2 scale 0.4}
#declare F_NVM=finish{ambient 0 diffuse 0.7 specular 0.01 roughness 0.001 reflection 0.1}
#declare T_PaintHead=texture{pigment{gradient y color_map{[0 C_NVM*0.5][1 C_NVM]}} normal{N_NVM} finish{F_NVM}}
#declare T_PaintBox=texture{pigment{gradient y color_map{[0 C_NVM*0.5][1 C_NVM]}} normal{N_NVM} finish{F_NVM}}


#declare T_USAToday=texture{
    pigment{image_map{gif "logo"}}
    normal{bozo 0.2}
    finish{ambient 0 diffuse 0.8 specular 0.1 roughness 0.05 }
}                       
// 170308 modify
//#declare NVM2=object{mNewsVM(xVMBox,yVMBox,zVMBox,yrtVMBox,eVM,T_PaintHead,T_PaintBox,T_NewsTop,T_NewsFront,T_NewsBottom)}

#declare NVM2=object{mNewsVM(xVMBox,yVMBox,zVMBox,yrtVMBox,eVM,T_PaintHead,T_PaintBox,T_NewsTop,T_NewsFront,T_NewsBottom,T_USAToday,T_USAToday,T_USAToday)}


//#declare xVMBox=0.49;
//#declare yVMBox=xVMBox*2.5/1.4;
//#declare zVMBox=0.45;
//#declare yrtVMBox=0.64;
//#declare C_NVM=rgb<1,0.1,0.05>*0.8; // red
//#declare C_NVM2=rgb<1,0.95,0.85>;
//#declare T_PaintHead=texture{pigment{gradient y color_map{[0 C_NVM2*0.5][1 C_NVM2]}} normal{N_NVM} finish{F_NVM}}
//#declare T_PaintBox=texture{pigment{gradient y color_map{[0 C_NVM*0.5][1 C_NVM]}} normal{N_NVM} finish{F_NVM}}
//#declare NVM3=object{mNewsVM(xVMBox,yVMBox,zVMBox,yrtVMBox,eVM,T_PaintHead,T_PaintBox,T_NewsTop,T_NewsFront,T_NewsBottom)}
//
//#declare xVMBox=0.40;
//#declare yVMBox=xVMBox*3.2/1.4;
//#declare zVMBox=0.4;
//#declare yrtVMBox=0.63;
//#declare C_NVM=rgb<0.141,0.9,0.25>*0.8; // green
//#declare T_PaintHead=texture{pigment{gradient y color_map{[0 C_NVM*0.5][1 C_NVM]}} normal{N_NVM} finish{F_NVM}}
//#declare T_PaintBox=texture{pigment{gradient y color_map{[0 C_NVM*0.5][1 C_NVM]}} normal{N_NVM} finish{F_NVM}}
//#declare NVM4=object{mNewsVM(xVMBox,yVMBox,zVMBox,yrtVMBox,eVM,T_PaintHead,T_PaintBox,T_NewsTop,T_NewsFront,T_NewsBottom)}


// -----------------------------------------
// USA Today vending machine
// -----------------------------------------

//#declare xV=1.75;
//#declare yV=xV*1.4/1.75;
//#declare rC=0.15;
//#declare eV=0.07;
//#declare zV=yV;
//#declare yF=xV*2.6/1.75;
//#declare rC2=rC+eV;
//#declare xF=xV*0.5/1.75;
//#declare T_VMHead=texture{
//    pigment{rgb<0.93,0.92,0.912>}
//    finish{ambient 0 diffuse 0.5 specular 0.01 roughness 0.01}
//}
//
//#declare T_VMFoot=texture{
//    pigment{
//        crackle solid
//        turbulence 0.3
//        scale 1/4
//        color_map{
//            [0 rgb<0.93,0.92,0.912>*0.1]
//            [1 rgb<0.93,0.92,0.912>*0.2]
//        }
//    }
//    normal{bozo 0.2}
//    finish{ambient 0 diffuse 0.8 specular 0.4 roughness 1/20}
//}                    
//#declare T_USAToday=texture{
//    pigment{image_map{gif "logo"}}
//    normal{bozo 0.2}
//    finish{ambient 0 diffuse 0.8 specular 0.1 roughness 0.05 }
//}                       
//#declare USAToday=box{0,1 texture{T_USAToday} translate <-0.5,-0.5,0> scale <213,142,1>/213}
//#declare NVM_UT=union{
//    // Head
//    union{
//        difference{cylinder{0,zV*z,rC2}cylinder{-z*0.1,zV*z*1.1,rC}plane{x,0 inverse}plane{y,0} translate <-xV/2,yV/2,0>}
//        difference{cylinder{0,zV*z,rC2}cylinder{-z*0.1,zV*z*1.1,rC}plane{x,0}plane{y,0} translate <xV/2,yV/2,0>}
//        difference{cylinder{0,zV*z,rC2}cylinder{-z*0.1,zV*z*1.1,rC}plane{x,0 inverse}plane{y,0 inverse} translate <-xV/2,-yV/2,0>}
//        difference{cylinder{0,zV*z,rC2}cylinder{-z*0.1,zV*z*1.1,rC}plane{x,0}plane{y,0 inverse} translate <xV/2,-yV/2,0>}
//        box{0,<xV,eV,zV> translate <-xV/2,yV/2+rC,0>}
//        box{0,<xV,eV,zV> translate <-xV/2,yV/2+rC,0> scale <1,-1,1>}
//        box{0,<eV,yV,zV> translate <xV/2+rC,-yV/2,0>}
//        box{0,<eV,yV,zV> translate <xV/2+rC,-yV/2,0> scale <-1,1,1>}
//        object{USAToday rotate z*45 scale xV/2 rotate y*90 translate <-xV/2-rC-eV*1.01,0,zV/2>}
//        
//        union{
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0 inverse}plane{y,0} translate <-xV/2,yV/2,0>}
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0}plane{y,0} translate <xV/2,yV/2,0>}
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0 inverse}plane{y,0 inverse} translate <-xV/2,-yV/2,0>}
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0}plane{y,0 inverse} translate <xV/2,-yV/2,0>}
//            cylinder{0,y*yV,eV/2 translate <-xV/2-eV/2-rC,-yV/2,0>}
//            cylinder{0,y*yV,eV/2 translate <xV/2+eV/2+rC,-yV/2,0>}
//            cylinder{0,x*xV,eV/2 translate <-xV/2,yV/2+eV/2+rC,0>}
//            cylinder{0,x*xV,eV/2 translate <-xV/2,-yV/2-eV/2-rC,0>}
//            scale <1,1,3>
//            texture{pigment{Black} finish{ambient 0 diffuse 0 specular 0.3 roughness 0.01 }}
//        }
//
//        union{
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0 inverse}plane{y,0} translate <-xV/2,yV/2,0>}
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0}plane{y,0} translate <xV/2,yV/2,0>}
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0 inverse}plane{y,0 inverse} translate <-xV/2,-yV/2,0>}
//            difference{torus{rC+eV/2,eV/2 rotate x*-90}plane{x,0}plane{y,0 inverse} translate <xV/2,-yV/2,0>}
//            cylinder{0,y*yV,eV/2 translate <-xV/2-eV/2-rC,-yV/2,0>}
//            cylinder{0,y*yV,eV/2 translate <xV/2+eV/2+rC,-yV/2,0>}
//            cylinder{0,x*xV,eV/2 translate <-xV/2,yV/2+eV/2+rC,0>}
//            cylinder{0,x*xV,eV/2 translate <-xV/2,-yV/2-eV/2-rC,0>}
//            union{
//                box{<-xV/2-rC-eV/2,-yV/2,0>,<xV/2+rC+eV/2,yV/2,eV>}
//                box{<-xV/2,-yV/2-rC-eV/2,0>,<xV/2,yV/2+rC+eV/2,eV>}
//                cylinder{0,eV*z,rC+eV/2 translate <-xV/2,yV/2,0>}
//                cylinder{0,eV*z,rC+eV/2 translate <xV/2,yV/2,0>}
//                cylinder{0,eV*z,rC+eV/2 translate <-xV/2,-yV/2,0>}
//                cylinder{0,eV*z,rC+eV/2 translate <xV/2,-yV/2,0>}
//                scale <1,1,-1>
//                translate z*eV/2
//            }
//            translate z*zV
//        }
//        union{
//            box{<-xV/2-rC-eV/2,-yV/2,0>,<xV/2+rC+eV/2,yV/2,eV>}
//            box{<-xV/2,-yV/2-rC-eV/2,0>,<xV/2,yV/2+rC+eV/2,eV>}
//            cylinder{0,eV*z,rC+eV/2 translate <-xV/2,yV/2,0>}
//            cylinder{0,eV*z,rC+eV/2 translate <xV/2,yV/2,0>}
//            cylinder{0,eV*z,rC+eV/2 translate <-xV/2,-yV/2,0>}
//            cylinder{0,eV*z,rC+eV/2 translate <xV/2,-yV/2,0>}
//            #declare yH=yV*0.7;
//            #declare zH=eV*2;
//            difference{
//                box{0,<eV,yH,zH> }
//                union{
//                    cylinder{-x*eV/2,x*eV*2,zH/2 translate y*zH}
//                    cylinder{-x*eV/2,x*eV*2,zH/2 translate y*(yH-zH)}
//                    box{<-eV/2,zH,-zH/2>,<eV*2,yH-zH,zH/2>}
//                    translate <0,0,zH>
//                }                     
//                translate <0.65*xV/2,-yV*0.2,0>
//                scale <0.5,1,-1>
//            }
//            translate z*eV
//            texture{pigment{image_map{gif "newsmap_1"}} finish{F_Newspaper} translate <-0.5,-0.5,0> scale <xV+rC*2,yV+rC*2,1>}
//        }
//        
//        texture{T_VMHead} 
//        translate <0,yF+yV/2,-zV/2>
//    }      
//    difference{  
//        superellipsoid{<0.3,0.3>}
//        plane{y,-0.5}
//        plane{y,0.5 inverse}
//        scale <xF*0.5,yF,xF*0.5>
//        translate y*yF/2
//        texture{T_VMFoot}
//    }                   
//    #declare VMFootElement=union{
//        cylinder{-x,x,rC}
//        box{<-1,-rC*2,-rC>,<1,0,rC>}
//        rotate x*10
//    }                                
//    union{  
//        box{<-xV/2,-1,-zV/2>,<xV/2,rC,zV/2>}
//        sphere{0,rC*0.5 translate <xV/2-rC,rC,zV/2-rC>}
//        sphere{0,rC*0.5 translate <-xV/2+rC,rC,zV/2-rC>}
//        sphere{0,rC*0.5 translate <xV/2-rC,rC,-zV/2+rC>}
//        sphere{0,rC*0.5 translate <-xV/2+rC,rC,-zV/2+rC>}
//        difference{object{VMFootElement scale <xV,1,1>}plane{x,0 rotate y*45 translate -x*xV/2}plane{x,0 rotate -y*45 inverse translate x*xV/2} translate -z*zV/2}
//        difference{object{VMFootElement scale <xV,1,1>}plane{x,0 rotate y*45 translate -x*xV/2}plane{x,0 rotate -y*45 inverse translate x*xV/2} scale <1,1,-1> translate z*zV/2}
//        difference{object{VMFootElement scale <zV,1,1>}plane{x,0 rotate y*45 translate -x*zV/2}plane{x,0 rotate -y*45 inverse translate z*zV/2} rotate y*-90 translate x*xV/2}
//        difference{object{VMFootElement scale <zV,1,1>}plane{x,0 rotate y*45 translate -x*zV/2}plane{x,0 rotate -y*45 inverse translate z*zV/2} rotate y*90 translate -x*xV/2}
//        translate y*rC
//        scale <1.2,0.4,1.2>
//        texture{T_VMFoot}
//    }
//    scale 0.6/xV
//}                             

// -----------------------------------------
// Scene file
// -----------------------------------------
global_settings{
    assumed_gamma 1
    radiosity{
        count 200 error_bound 0.2
        recursion_limit 2
    }
}
//------------------------------ the Axes --------------------------------
//------------------------------------------------------------------------
#macro Axis_( AxisLen, Dark_Texture,Light_Texture) 
 union{
    cylinder { <0,-AxisLen,0>,<0,AxisLen,0>,0.05
               texture{checker texture{Dark_Texture } 
                               texture{Light_Texture}
                       translate<0.1,0,0.1>}
             }
    cone{<0,AxisLen,0>,0.2,<0,AxisLen+0.7,0>,0
          texture{Dark_Texture}
         }
     } // end of union                   
#end // of macro "Axis()"
//------------------------------------------------------------------------
#macro AxisXYZ( AxisLenX, AxisLenY, AxisLenZ, Tex_Dark, Tex_Light)
//--------------------- drawing of 3 Axes --------------------------------
union{
#if (AxisLenX != 0)
 object { Axis_(AxisLenX, Tex_Dark, Tex_Light) scale 0.3 rotate< 0,0,-90>}// x-Axis
 text   { ttf "crystal.ttf",  "x",  0.15,  0  texture{Tex_Dark} 
          rotate<10,-45,0> scale 0.35 translate <AxisLenX+0.05,0.4,-0.10> no_shadow}
#end // of #if 
#if (AxisLenY != 0)
 object { Axis_(AxisLenY, Tex_Dark, Tex_Light) scale 0.5  rotate< 0,0,  0>}// y-Axis
 text   { ttf "crystal.ttf",  "y",  0.15,  0  texture{Tex_Dark}    
          rotate<10,0,0> scale 0.60 translate <-0.65,AxisLenY+0.50,-0.10>  rotate<0,-45,0> no_shadow}
#end // of #if 
#if (AxisLenZ != 0)
 object { Axis_(AxisLenZ, Tex_Dark, Tex_Light)   rotate<90,0,  0>}// z-Axis
 text   { ttf "crystal.ttf",  "z",  0.15,  0  texture{Tex_Dark}
          rotate<10,-45,0> scale 1.0 translate <-0.75,0.2,AxisLenZ+0.10> no_shadow}
#end // of #if 
} // end of union
#end// of macro "AxisXYZ( ... )"
//------------------------------------------------------------------------

#declare Texture_A_Dark  = texture {
                               pigment{ color rgb<1,0.45,0>}
                               finish { phong 1}
                             }
#declare Texture_A_Light = texture { 
                               pigment{ color rgb<1,1,1>}
                               finish { phong 1}
                             }

object{ AxisXYZ( 3.25, 2.2, 8, Texture_A_Dark, Texture_A_Light)}
//-------------------------------------------------- end of coordinate axes
camera{
    //location  <0.0, 1.8, -6>
    //direction 3*z
	location <3.0, 1.8,10>
	direction 3*z
    right     4*x/3
    look_at   <0.0, 0.8, 0.0>
}
//background{White}
background{rgb <150,200,255>/255}
light_source{-z*1000 color rgb<255,240,200>*2.5/255 rotate x*45 rotate -y*70
    area_light 20*x,20*z 8,8 jitter adaptive 2
}
union{
    //object{NVM_UT translate -x*2}
    object{NVM2 translate <-0.8,0,0.1>}
    //object{NVM3}
    //object{NVM4 translate <0.8,0,-0.1>}
    rotate y*-45
    translate z*2+x*0.7
}
plane{y,0 texture{pigment{White*0.3}finish{ambient 0 diffuse 1}}}
 



