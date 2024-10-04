//This_working_process need 1.Two folder: first is data folder, another is outpur folder 2. code work for 'tif' image file


dir = getDirectory("Choose_data_Directory ");
dir2 = getDirectory("Choose_Destination_Directory ") //outoput folder has to be located in seprately location of working folder
   
   setBatchMode(true);
   count = 0;
   countFiles(dir);
   n = 0;
   processFiles(dir);
   //print(count+" files processed");
   
   function countFiles(dir) {
      list = getFileList(dir);
      for (i=0; i<list.length; i++) {
          if (endsWith(list[i], "/"))
              countFiles(""+dir+list[i]);
          else
              count++;
      }
  }

   function processFiles(dir) {
      list = getFileList(dir);
      for (i=0; i<list.length; i++) {
          if (endsWith(list[i], "/"))
              processFiles(""+dir+list[i]);
          else {
             showProgress(n++, count);
             //print("Hello");
             path = dir+list[i];
             processFile(path);
          }
      }
  }

  function processFile(path) {
       if (endsWith(path, ".tif")) {
           open(path);
           setOption("ScaleConversions", true);
           run("8-bit");
           run("Make Binary", "background=Dark calculate black");
           run("Erode", "stack");
           //print(list[i][3]);
           saveAs("tiff", dir2 + list[i]);
           close();
      }
  }
