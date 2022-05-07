{
    app.beginSuppressDialogs();
    var output = new File("output.txt");
    output.open("r");   
    // get project path
    var data = output.read();
    var data_arr = data.split(';');
    var project_path = data_arr[0];
    var compName = data_arr[1];
    var output_path = data_arr[2];
    var myProject = File(project_path);
    // open aep project
    app.open(myProject);
    output.close();  
    // remove output file
    output.remove();

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
        // Important! create 'MP3' tamplate in After Effects before running the script!
        // rendering only audio file for composition
        var outTemp = comp.outputModule(1);
        outTemp.applyTemplate("WAV");
        // set output path
        var output_data = {
            "Output File Info": {
                "Full Flat Path": output_path
            }
        };
        outTemp.setSettings( output_data );
        path = outTemp.file.path + '/' + outTemp.file.name;
        app.project.renderQueue.render();
    }

    var newOutput = new File("output.txt");
    newOutput.open("w");   
    newOutput.encoding = "UTF-8";
    newOutput.write(path);
    newOutput.close();
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}