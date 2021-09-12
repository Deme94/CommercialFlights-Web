<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Vuelo;
use App\Aeropuerto;
use App\Aerolinea;
use DB;
use Exception;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;
use Carbon\Carbon;


class VueloController extends Controller
{
    /**
     * @OA\Get(path="/api/vuelos",
     *   summary="Mostrar la información principal de los vuelos por orden de fecha.",
     *   tags={"Vuelos"},
     *        @OA\Response(
     *         response=200,
     *         description="Devuelve la información principal de los vuelos por orden de fecha correctamente.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="id", type="integer"),
     *                  @OA\Property(property="código_vuelo", type="string"),
     *                  @OA\Property(property="siglas_aeropuerto_salida", type="string"),
     *                  @OA\Property(property="nombre_aerolínea", type="string"),
     *                  @OA\Property(property="aeropuerto_destino", type="string"),
     *                  @OA\Property(property="date_time", type="date"),
     *                  @OA\Property(property="hora_programada", type="string"),
     *                  @OA\Property(property="hora_salida", type="string"),
     *                  @OA\Property(property="estado", type="int"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Error: Internal Server Error."))
     */

    public function getVuelos(){
        $vuelos = DB::select(DB::raw("select vuelos.id, vuelos.codigo_vuelo, aeropuertos.siglas, aerolineas.nombre as aerolinea, vuelos.aeropuerto_destino, vuelos.date_time, vuelos.hora_programada, vuelos.hora_salida, vuelos.estado
            from vuelos
            INNER JOIN aeropuertos ON vuelos.id_aeropuerto_salida=aeropuertos.id
            INNER JOIN aerolineas ON vuelos.id_aerolinea=aerolineas.id
            ORDER BY vuelos.date_time DESC
        "));
        return $vuelos;
    }

    /**
     * @OA\Get(path="/api/vuelos/tabla/{id_aeropuerto}",
     *   summary="Mostrar la información principal de los vuelos de la fecha actual.",
     *   tags={"Vuelos"},
     *        @OA\Parameter(
     *         name = "id_aeropuerto",
     *         description = "Identificador del vuelo asignado en la base de datos.",
     *         required  = true,
     *         in = "path",
     *         @OA\Schema(
     *              type="integer"    
     *              ) 
     *         ),
     *        @OA\Response(
     *         response=200,
     *         description="Devuelve la información principal de los vuelos de la fecha actual de la petición.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="código_vuelo", type="string"),
     *                  @OA\Property(property="nombre_aerolínea", type="string"),
     *                  @OA\Property(property="siglas_aeropuerto_salida", type="string"),
     *                  @OA\Property(property="hora_programada", type="string"),
     *                  @OA\Property(property="hora_salida", type="string"),
     *                  @OA\Property(property="estado", type="int"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Error: Internal Server Error."))
     */

    public function getVuelos_tabla_id($id_aeropuerto) {
        $vuelos = DB::select(DB::raw("select vuelos.codigo_vuelo, aerolineas.nombre as aerolinea, vuelos.hora_programada, vuelos.hora_salida, vuelos.estado from vuelos
        INNER JOIN aerolineas ON vuelos.id_aerolinea=aerolineas.id
        INNER JOIN aeropuertos ON vuelos.id_aeropuerto_salida=aeropuertos.id
        WHERE aeropuertos.id = '$id_aeropuerto' AND vuelos.date_time = CURDATE()"));
        return $vuelos;

    }

    /**
     * @OA\Get(path="/api/vuelos/{codigo_vuelo}/{id_aeropuerto}/{fecha}",
     *   summary="Mostrar la información recopilada de un vuelo específico buscado.",
     *   tags={"Vuelos"},
     *        @OA\Parameter(
     *         name = "codigo_vuelo",
     *         description = "Código de vuelo asignado.",
     *         required  = true,
     *         in = "path",
     *         @OA\Schema(
     *              type="string"    
     *              ) 
     *         ),
     *         @OA\Parameter(
     *         name = "id_aeropuerto",
     *         description = "Identificador del vuelo asignado en la base de datos.",
     *         required  = true,
     *         in = "path",
     *         @OA\Schema(
     *              type="integer"    
     *              ) 
     *         ),
     *         @OA\Parameter(
     *         name = "fecha",
     *         description = "Fecha de salida del vuelo.",
     *         required  = true,
     *         in = "path",
     *         @OA\Schema(
     *              type="string"    
     *          ) 
     *        ),
     *        @OA\Response(
     *         response=200,
     *         description="Devuelve la información principal de un vuelo específico, a través del su código, fecha y aeropuertos de salida.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="código_vuelo", type="string"),
     *                  @OA\Property(property="nombre_aerolínea", type="string"),
     *                  @OA\Property(property="nombre_aeropuerto", type="string"),
     *                  @OA\Property(property="siglas_aeropuerto_salida", type="string"),
     *                  @OA\Property(property="aeropuerto_destino", type="string"),
     *                  @OA\Property(property="terminal", type="string"),
     *                  @OA\Property(property="hora_programada", type="string"),
     *                  @OA\Property(property="hora_salida", type="string"),
     *                  @OA\Property(property="estado", type="int"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Error: Internal Server Error."))
     */

    public function getInfoVuelos_espec($codigo_vuelo, $id_aeropuertos, $fecha) {
        $info_vuelos = DB::select(DB::raw("select vuelos.codigo_vuelo, aerolineas.nombre as aerolinea, aeropuertos.nombre, aeropuertos.siglas, vuelos.aeropuerto_destino, vuelos.terminal, vuelos.hora_programada, vuelos.hora_salida, vuelos.estado from vuelos
        INNER JOIN aerolineas ON vuelos.id_aerolinea=aerolineas.id
        INNER JOIN aeropuertos ON vuelos.id_aeropuerto_salida=aeropuertos.id
        WHERE vuelos.codigo_vuelo = '$codigo_vuelo' AND aeropuertos.id = '$id_aeropuertos' AND vuelos.date_time = '$fecha'"));
        return $info_vuelos;
    }

    /**
    * @OA\Post(
    *     path="/api/vuelos",
    *     summary="Almacenar vuelos",
    *     tags={"Vuelos"},
    *     @OA\RequestBody(
    *           description= "Vuelos del web scraper.",
    *           required= true,
    *           @OA\JsonContent(
    *               type="object",
    *               @OA\Property(property="aeropuerto", type="string"),
    *                * @OA\Property(
        *                  type="array",
        *                  @OA\Items(
                    *               @OA\Property(property="fecha", type="string"),
                    *               @OA\Property(property="codigoVuelo", type="string"),
                    *               @OA\Property(property="destino", type="string"),
                    *               @OA\Property(property="aerolinea", type="integer"),
                    *               @OA\Property(property="horaProgramada", type="number"),
                    *               @OA\Property(property="horaReal", type="integer"),
                    *               @OA\Property(property="estado", type="integer"),
                    *               @OA\Property(property="terminal", type="integer"),
                    *               @OA\Property(property="distancia", type="integer"),

        *                  ),
    *              )
    *           )
    *     ),
    *     @OA\Response(
    *         response=200,
    *         description="Almacena todos los vuelos. Si ya existen, se actualizan sus estados y horas programadas.",
    *           @OA\JsonContent(
    *               type="object",
                    *               @OA\Property(property="id", type="integer"),
                    *               @OA\Property(property="fecha", type="string"),
                    *               @OA\Property(property="codigo_vuelo", type="string"),
                    *               @OA\Property(property="aeropuerto_destino", type="string"),
                    *               @OA\Property(property="id_aerolinea", type="integer"),
                    *               @OA\Property(property="id_aeropuerto_salida", type="integer"),
                    *               @OA\Property(property="hora_programada", type="string"),
                    *               @OA\Property(property="hora_salida", type="string"),
                    *               @OA\Property(property="estado", type="integer"),
                    *               @OA\Property(property="terminal", type="string"),
                    *               @OA\Property(property="distancia", type="integer"),
    *           )
    *     ),
    *           @OA\Response(response=400, description="Error: Bad Request."),
    *           @OA\Response(response=500, description="Error: Internal Server Error."))
    * )
    */

    public function store(Request $request){
        $lista = array();
        $arrayVuelos = $request->json()->all();
        foreach ($arrayVuelos as $aeropuerto => $value) {
            foreach ($arrayVuelos[$aeropuerto] as $vuelo1 => $value2) {

                $vuelo = new Vuelo();

                $id = Aeropuerto::select('id')->where('siglas', $aeropuerto)->get();
                $vuelo->id_aeropuerto_salida = $id[0]['id'];
                $vuelo->date_time = $arrayVuelos[$aeropuerto][$vuelo1]['fecha'];
                $vuelo->codigo_vuelo = $arrayVuelos[$aeropuerto][$vuelo1]['codigoVuelo'];
                $vuelo->aeropuerto_destino = $arrayVuelos[$aeropuerto][$vuelo1]['destino'];

                $aerolinea = $arrayVuelos[$aeropuerto][$vuelo1]['aerolinea'];
                $id = Aerolinea::select('id')->where('nombre', $aerolinea)->get();
                $vuelo->id_aerolinea = $id[0]['id'];

                $vuelo->hora_programada = $arrayVuelos[$aeropuerto][$vuelo1]['horaProgramada'];
                $vuelo->hora_salida = $arrayVuelos[$aeropuerto][$vuelo1]['horaReal'];
                $vuelo->estado = $arrayVuelos[$aeropuerto][$vuelo1]['estado'];
                $vuelo->terminal = $arrayVuelos[$aeropuerto][$vuelo1]['terminal'];
                $vuelo->distancia = $arrayVuelos[$aeropuerto][$vuelo1]['distancia'];
                if(count(Vuelo::select('id')->where('date_time', $vuelo->date_time)->where('codigo_vuelo', $vuelo->codigo_vuelo)->where('id_aerolinea', $vuelo->id_aerolinea)->get())>0){
                    Vuelo::where('date_time', $vuelo->date_time)->where('codigo_vuelo', $vuelo->codigo_vuelo)->where('id_aerolinea', $vuelo->id_aerolinea)->update(array('estado' => $vuelo->estado, 'hora_salida' => $vuelo->hora_salida));

                    error_log('Ya existe. Estado de vuelo actualizado.');
                } else {
                	array_push($lista, $vuelo->toArray());
                    $vuelo->save();  // Guarda en la base de datos (hace un insert)

            	}
                //$vuelo->save();  // Guarda en la base de datos (hace un insert)
            }
        }
        try{
            //Vuelo::insert($lista);
            error_log('Vuelos subidos.');
        }
        catch(Exception $e)
        {
           error_log($e->getMessage());
        }
    }

    /**
     * @OA\Get(path="/api/vuelos/predecir/{estado}",
     *   summary="Recoge toda la información asociada a un id de un vuelo.",
     *   tags={"Vuelos"},
     *        @OA\Parameter(
     *         name = "estado",
     *         description = "Datos que indica el estado del vuelo.",
     *         required  = true,
     *         in = "path",
     *         @OA\Schema(
     *              type="integer"    
     *              ) 
     *         ),
     *        @OA\Response(
     *         response=200,
     *         description="Devuelta la información de las predicciones de los vuelos de manera correcta.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="id_vuelo", type="integer"),
     *                  @OA\Property(property="id_aerolinea", type="integer"),
     *                  @OA\Property(property="id_aeropuerto", type="integer"),
     *                  @OA\Property(property="date_time", type="date"),
     *                  @OA\Property(property="hora_programada", type="string"),
     *                  @OA\Property(property="hora_salida", type="string"),
     *                  @OA\Property(property="cielo", type="string"),
     *                  @OA\Property(property="temperatura", type="integer"),
     *                  @OA\Property(property="lluvia", type="double"),
     *                  @OA\Property(property="porcentajeLluvia", type="integer"),
     *                  @OA\Property(property="nubes", type="integer"),
     *                  @OA\Property(property="viento", type="integer"),
     *                  @OA\Property(property="rafaga", type="integer"),
     *                  @OA\Property(property="direccion_viento", type="string"),
     *                  @OA\Property(property="humedad", type="integer"),
     *                  @OA\Property(property="presion", type="integer"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Error: Internal Server Error."))
     */

    public function getDatosPrediccion($estado)
    {
        $vuelos = DB::select(DB::raw("select vuelos.id as id_vuelo,
            id_aerolinea, id_aeropuerto_salida, vuelos.date_time, aeropuerto_destino,
            codigo_vuelo, terminal, distancia, hora_programada, hora_salida, clima.cielo, clima.temperatura, clima.lluvia, clima.porcentajeLluvia, clima.nubes, clima.viento, clima.rafaga, clima.direccion_viento, clima.humedad, clima.presion
         from vuelos
            INNER JOIN clima
            ON vuelos.id_aeropuerto_salida = clima.id_aeropuerto AND
                vuelos.date_time = clima.date_time AND
                ABS(time_to_sec(STR_TO_DATE(vuelos.hora_programada ,'%H:%i'))+1-time_to_sec(STR_TO_DATE(clima.hora,'%H:%i')))<1800
                WHERE vuelos.estado = :estado
                GROUP BY id_vuelo, id_aerolinea, id_aeropuerto_salida, vuelos.date_time, aeropuerto_destino, codigo_vuelo, terminal, distancia, hora_programada, hora_salida, clima.cielo, clima.temperatura, clima.lluvia, clima.porcentajeLluvia, clima.nubes, clima.viento, clima.rafaga, clima.direccion_viento, clima.humedad, clima.presion;"),array('estado' => $estado));

        return $vuelos;
    }

    public function actualizarEstimaciones(Request $request)
    {
        $arrayVuelos = $request->json()->all();
        foreach ($arrayVuelos as $estimacion => $value) {
            Vuelo::where('id', $estimacion)->update(array('hora_salida' => $arrayVuelos[$estimacion]));
        }
        error_log('Estimaciones actualizadas');
    }

    public function estaRecopilando(){
        error_log('Recopilando vuelos = '.Cache::get('recopilando'));
        $tiempoRecopilando = Carbon::now()->timestamp-Cache::get('tiempoRecopilar');
        return [Cache::get('recopilando'), $tiempoRecopilando];
    }

    public function recopilar(){
        $response = Http::get('http://localhost:8000/api/vuelos/recopilar/start');
        ini_set('max_execution_time', 6000);
        error_log("Recopilando clima y vuelos...");
        $cmd = "python ".storage_path("/ejecutables/Main.py"." 2>&1");
        error_log(shell_exec($cmd));
        $response = Http::get('http://localhost:8000/api/vuelos/recopilar/stop');
    }

    public function startRecopilar(){
        error_log("START");
        Cache::add('recopilando', '0');
        Cache::put('tiempoRecopilar', Carbon::now()->timestamp);
        Cache::put('recopilando', '1');
    }
    public function stopRecopilar(){
        error_log("STOP");
        Cache::put('recopilando', '0');
    }
}
