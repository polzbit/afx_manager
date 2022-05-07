{
    app.beginSuppressDialogs();
    var output = new File("output.txt");
    output.open("r");   
    var data = output.read();
    var data_arr = data.split(';');
    var first_frame_file = data_arr[0];
    var format = data_arr[1];
    var fps = parseFloat(data_arr[2]);
    var audio = data_arr[3].toString();
    var output_path = data_arr[4];
    var duration = parseFloat(data_arr[5]);
    output.close();  
    output.remove();
    var path = 'error'
    // creating new composition based on psd sequence
    var io = new ImportOptions(new File(first_frame_file));
    if (io.canImportAs(ImportAsType.COMP)) {
        io.importAs = ImportAsType.COMP;
        io.sequence = true;
        var item = app.project.importFile(io);
        var compName = item.file.name.toString();
        var extFind = compName.lastIndexOf(".");
        var seqFind = compName.lastIndexOf("_");
        var fileWithoutExt = compName.substring(extFind, 0);     //Removes file extension
        var filenameOnly = fileWithoutExt.substring(seqFind, 0); 
        var newComp = app.project.items.addComp(filenameOnly, item.width, item.height, item.pixelAspect, duration, fps);
        // check and add audio if needed
        if(audio!= '0' && audio != '' && audio != 'None') {
            var aud_file = new File(audio);
            if(aud_file.exists === true) {
                var audio_item = app.project.importFile(new ImportOptions(aud_file)); 
                newComp.layers.add(audio_item);
                // todo check when audio layer has been added
                $.sleep(2000);
            }
        }
        // adding composition to render queue
        var queueComp = app.project.renderQueue.items.add(newComp);
        queueComp.applyTemplate("Best Settings");
        queueComp.render = true;
        var outTemp = queueComp.outputModule(1);
        outTemp.applyTemplate(format);
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