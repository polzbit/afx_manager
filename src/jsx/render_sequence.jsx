{
    app.beginSuppressDialogs();
    var output = new File("output.txt");
    output.open("r");   
    var data = output.read();
    var data_arr = data.split(';');
    var proj_path = data_arr[0];
    var compName = data_arr[1];
    var fps = data_arr[2];
    var output_path = data_arr[3];  // folder of output frames
    output.close();
    output.remove();

    var myProject = File(proj_path);
    // open aep project
    app.open(myProject);
    // finding composition
    var comp = null;
    for(var i = 1; i <= app.project.renderQueue.numItems; i++){
        var queueComp = app.project.renderQueue.item(i);
        queueComp.render = false;
        if (queueComp.comp.name == compName) {
            comp = queueComp;
            comp.render = true;
        }
    }
    var path = 'error'
    if(comp) {        
        comp.applyTemplate("Multi-Machine Settings");
        comp.frameRate = fps;
        var outTemp = comp.outputModule(1);
        // set output path
        var output_data = {
            "Output File Info": {
                "Full Flat Path": output_path
            }
        };
        outTemp.setSettings( output_data );
        outTemp.applyTemplate("Multi-Machine Sequence");
        
        path = outTemp.file.path + '/' + outTemp.file.name;
        app.project.renderQueue.render();
        
    } 
        
    var NewOutput = new File("output.txt");
    NewOutput.open("w");   
    NewOutput.encoding = "UTF-8";
    NewOutput.write(path);
    NewOutput.close();
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}