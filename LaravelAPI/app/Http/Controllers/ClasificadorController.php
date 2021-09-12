<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;
use Carbon\Carbon;

class ClasificadorController extends Controller
{
    public function getModelo(){
    	return json_decode(file_get_contents(storage_path('/ejecutables/model.json')), true);
    }

    public function estaEntrenando(){
        error_log('Entrenando = '.Cache::get('entrenando'));
        $tiempoEntrenando = Carbon::now()->timestamp-Cache::get('tiempoEntrenar');
        return [Cache::get('entrenando'), $tiempoEntrenando];
    }

    public function entrenar(){
        $response = Http::get('http://localhost:8000/api/clasificador/entrenar/start');
        ini_set('max_execution_time', 6000);
        error_log("Entrenando nuevo modelo...");
        $cmd = "python ".storage_path("/ejecutables/Entrenamiento.py"." 2>&1");
        error_log(shell_exec($cmd));
        $response = Http::get('http://localhost:8000/api/clasificador/entrenar/stop');
    }

    public function startEntrenar(){
        error_log("START");
        Cache::add('entrenando', '0');
        Cache::put('tiempoEntrenar', Carbon::now()->timestamp);
        Cache::put('entrenando', '1');
    }
    public function stopEntrenar(){
        error_log("STOP");
        Cache::put('entrenando', '0');
    }
}
