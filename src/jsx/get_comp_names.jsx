{
    app.beginSuppressDialogs();
    var output = new File("output.txt");
    output.open("r");   
    var path = output.read();
    var myProject = File(path);
    app.open(myProject);
    output.close();  
    output.remove();

    var comps_str = "";
    for(var i = 1; i <= app.project.renderQueue.numItems; i++){
        queueComp = app.project.renderQueue.item(i);
        fps = queueComp.comp.frameDuration
        comps_str += queueComp.comp.name + "|" + queueComp.comp.duration  + "|" + fps + "\n";
    }
    var newOutput = new File("output.txt");
    newOutput.open("w");   
    newOutput.encoding = "UTF-8";
    newOutput.write(comps_str);
    newOutput.close();
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}