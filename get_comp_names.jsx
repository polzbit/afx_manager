{
    app.beginSuppressDialogs();
    var file = new File("output.txt");
    file.open("r");   
    var path = file.read();
    var myProject = File(path);
    app.open(myProject);
    file.close();  
    file.remove();

    comps_str = "";
    for(var i = 1; i <= app.project.renderQueue.numItems; i++){
        queueComp = app.project.renderQueue.item(i);
        if(queueComp.status == RQItemStatus.QUEUED) {
            comps_str += queueComp.comp.name + "|" + queueComp.timeSpanDuration + "|" + queueComp.comp.frameDuration + "\n";
        }
    }
    file = new File("output.txt");
    file.open("w");   
    file.encoding = "UTF-8";
    file.write(comps_str);
    file.close();
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}