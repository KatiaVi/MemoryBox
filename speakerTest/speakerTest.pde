/**
  * This sketch demonstrates how to play a file with Minim using an AudioPlayer. <br />
  * It's also a good example of how to draw the waveform of the audio. Full documentation 
  * for AudioPlayer can be found at http://code.compartmental.net/minim/audioplayer_class_audioplayer.html
  * <p>
  * For more information about Minim and additional features, 
  * visit http://code.compartmental.net/minim/
  */

import ddf.minim.*;
import ddf.minim.ugens.*;
import java.io.File;
import static java.lang.System.out;
import java.util.Arrays; 
import processing.sound.*; 


Minim minim;
AudioPlayer player;
AudioPlayer player2;
File dir; 
String[] files; 
Reverb reverb; 

boolean isPlayerDecreasing = true; 
boolean isPlayer2Decreasing = false; 
boolean startPlaying = true;

int index = 0; 

void setup()
{
  size(512, 200, P3D);
  
  // we pass this to Minim so that it can load files from the data directory
  minim = new Minim(this);
  dir = new File(dataPath(""));
  files = dir.list(); 

   

  System.out.println(Arrays.toString(files)); 

  player = minim.loadFile(files[0]);
  player.setPan(1);  
}

void draw()
{
  background(0);
  stroke(255);
  
  // draw the waveforms
  // the values returned by left.get() and right.get() will be between -1 and 1,
  // so we need to scale them up to see the waveform
  // note that if the file is MONO, left.get() and right.get() will return the same value
  for(int i = 0; i < player.bufferSize() - 1; i++)
  {
    float x1 = map( i, 0, player.bufferSize(), 0, width );
    float x2 = map( i+1, 0, player.bufferSize(), 0, width );
    line( x1, 50 + player.left.get(i)*50, x2, 50 + player.left.get(i+1)*50 );
    line( x1, 150 + player.right.get(i)*50, x2, 150 + player.right.get(i+1)*50 );
  }
  
  // draw a line to show where in the song playback is currently located
  float posx = map(player.position(), 0, player.length(), 0, width);
  stroke(0,200,0);
  line(posx, 0, posx, height);
  
  if ( player.isPlaying() )
  {
    text("Press any key to pause playback.", 10, 20 );
  }
  else
  {
    text("Press any key to start playback.", 10, 20 );
  }
  
  if (player.getPan()-0.015 <= -1) { 
      player.setPan(player.getPan()+0.015); 
      isPlayerDecreasing = false; 
    }
    else if (player.getPan() + 0.015 >= 1) { 
      player.setPan(player.getPan()-0.015); 
      isPlayerDecreasing = true;
    } 
    else if (isPlayerDecreasing) { 
      player.setPan(player.getPan()-0.015); 
    } 
    else { 
      player.setPan(player.getPan()+0.015); 
    } 
    
    if (files[(index+1)%files.length].equals(".DS_Store")) { 
      index += 1; 
    }
    
    if (!player.isPlaying()) { 
      String path = files[(index+1)%files.length];
      player = minim.loadFile(path); 
      index += 1;
      player.play(); 
    }
  
}

void keyPressed()
{
  if ( player.isPlaying() )
  {
    player.pause(); 
  }
  else if ( player.position() == player.length() )
  {
    player.rewind();
    
    player.play();

  }
  else
  {
    player.play();
  }

}