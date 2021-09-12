<?php

namespace App\Http\Controllers;

use App\Aerolinea;
use Exception;
use Illuminate\Http\Request;
use DB;

class AerolineaController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */

    /**
     * @OA\Get(path="/api/aerolineas",
     *     summary="Mostrar lista de aerolineas",
     *     tags={"Aerolíneas"},
     *     @OA\Response(
     *         response=200,
     *         description="Devuelve todas las aerolíneas almacenadas.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="id", type="integer"),
     *                  @OA\Property(property="nombre", type="string"),
     *                  @OA\Property(property="puntuacion", type="string"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Error: Internal Server Error."))
     */
    public function index()
    {
        $aerolineas = Aerolinea::select('id','nombre','puntuacion')->get();
        return $aerolineas;
    }

    /**
     * @OA\Get(path="/api/aerolineas/top",
     *     summary="Mostrar lista de las 10 mejores aerolineas",
     *     tags={"Aerolíneas"},
     *         @OA\Response(
     *         response=200,
     *         description="Devuelve todas las 10 aerolíneas almacenadas en función de su valoración.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="id", type="integer"),
     *                  @OA\Property(property="nombre", type="string"),
     *                  @OA\Property(property="puntuacion", type="string"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Internal Server Error."))
     */
    public function getTopScore(){
        $top = Aerolinea::select('id','nombre','puntuacion')->get()->sortByDesc("puntuacion")->take(10);
        return $top;
    }

    /**
     * @OA\Get(path="/api/aerolineas/{id_aeropuerto}",
     *   summary="Mostrar la información principal de los vuelos de la fecha actual, ordenada por valoración de aerolíneas de mayor a menor.",
     *   tags={"Aerolíneas"},
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
     *         description="Devuelve la información principal de los vuelos ordenados por valoración de aerolíneas.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="código_vuelo", type="string"),
     *                  @OA\Property(property="nombre_aerolínea", type="string"),
     *                  @OA\Property(property="hora_programada", type="string"),
     *                  @OA\Property(property="hora_salida", type="string"),
     *                  @OA\Property(property="estado", type="int"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Error: Internal Server Error."))
     */

    public function getAerolineasXpuntuacion($id_aeropuertos) {
        $vuelos_mejores_aerolineas = DB::select(DB::raw("select vuelos.codigo_vuelo, aerolineas.nombre as aerolinea, vuelos.hora_programada, vuelos.hora_salida, vuelos.estado from vuelos
        INNER JOIN aerolineas ON vuelos.id_aerolinea=aerolineas.id
        INNER JOIN aeropuertos ON vuelos.id_aeropuerto_salida=aeropuertos.id
        WHERE aeropuertos.id = '$id_aeropuertos' AND vuelos.date_time = CURDATE()
        ORDER BY aerolineas.puntuacion desc"));
        return $vuelos_mejores_aerolineas;
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */

    /**
    * @OA\Post(
    *     path="/api/aerolineas",
    *     summary="Almacenar aerolineas",
    *     tags={"Aerolíneas"},
    *     @OA\RequestBody(
    *           description= "Aerolíneas web scraper.",
    *           required= true,
    *           @OA\JsonContent(
    *               @OA\Property(property="nombre", type="string"),
    *           ),
    *     ),
    *     @OA\Response(
    *         response=200,
    *         description="Almacena todas las aerolíneas.",
    *           @OA\JsonContent(
    *               type="array",
                    *        @OA\Items(
                    *               @OA\Property(property="id", type="integer"),
                    *               @OA\Property(property="nombre", type="string"),
                    *               @OA\Property(property="puntuacion", type="number"),
                    *        )
    *           )
    *     ),
    *           @OA\Response(response=400, description="Error: Bad Request."),
    *           @OA\Response(response=500, description="Error: Internal Server Error."))
    * )
    */


    public function store(Request $request)
    {
        $lista = array();
        $arrayAerolineas = $request->json()->all();
        foreach ($arrayAerolineas as $key => $value) {
            $aerolinea = new Aerolinea();
            $aerolinea->nombre = $arrayAerolineas[$key];
            array_push($lista, $aerolinea->toArray());
        }
        try{
            Aerolinea::insert($lista);
            error_log('Aerolineas subidas.');
        }
        catch(Exception $e)
        {
           error_log($e->getMessage());
        }
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Aerolinea  $aerolinea
     * @return \Illuminate\Http\Response
     */

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Aerolinea  $aerolinea
     * @return \Illuminate\Http\Response
     */
    public function edit(Aerolinea $aerolinea)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Aerolinea  $aerolinea
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Aerolinea $aerolinea)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Aerolinea  $aerolinea
     * @return \Illuminate\Http\Response
     */
    public function destroy(Aerolinea $aerolinea)
    {
        //
    }
}
