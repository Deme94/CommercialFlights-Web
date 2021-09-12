<?php

namespace App\Http\Controllers;

use App\Aeropuerto;
use Illuminate\Http\Request;

class AeropuertoController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */

    /**
     * @OA\Get(path="/api/aeropuertos",
        *   summary="Mostrar lista de aeropuertos con toda su información.",
        *   tags={"Aeropuertos"},
     *         @OA\Response(
     *         response=200,
     *         description="Devuelve toda la información de todos los aeropuertos almacenados.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="id", type="integer"),
     *                  @OA\Property(property="nombre", type="string"),
     *                  @OA\Property(property="ciudad", type="string"),
     *                  @OA\Property(property="siglas", type="string"),
     *                  @OA\Property(property="puntuacion", type="number"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error en la consulta."),
     * @OA\Response(response=404, description="Not Found."))
     */
    public function index()
    {
        $aeropuertos = Aeropuerto::select('id','nombre','ciudad','siglas','puntuacion')->get();
        return $aeropuertos;
    }

    /**
     * @OA\Get(path="/api/aeropuertos/nombre",
        *   summary="Mostrar lista de nombres y siglas de aeropuertos",
        *   tags={"Aeropuertos"},
     *         @OA\Response(
     *         response=200,
     *         description="Devuelve todas los aeropuertos con sus siglas almacenadas.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="id", type="integer"),
     *                  @OA\Property(property="nombre", type="string"),
     *                  @OA\Property(property="siglas", type="string"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error en la consulta."),
     * @OA\Response(response=404, description="Not Found."))
     */

    public function mostrarNombreAeropuertos() {
        $aeropuertos = Aeropuerto::select('id', 'nombre', 'siglas')->get();
        return $aeropuertos;
    }

    /**
     * @OA\Get(path="/api/aeropuertos/top",
     *   summary="Mostrar lista de los 10 mejores aeropuertos por valoración",
     *   tags={"Aeropuertos"},
     *        @OA\Response(
     *         response=200,
     *         description="Devuelve el top de los 10 mejores aeropuertos por valoración.",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                  @OA\Property(property="id", type="integer"),
     *                  @OA\Property(property="nombre", type="string"),
     *                  @OA\Property(property="ciudad", type="string"),
     *                  @OA\Property(property="siglas", type="string"),
     *                  @OA\Property(property="puntuacion", type="number"),
     *              )
     *         )
     *     ),
     * @OA\Response(response=400, description="Error: Bad Request."),
     * @OA\Response(response=500, description="Error: Internal Server Error."))
     */

    public function getTopScore(){
        $top = Aeropuerto::select('id','nombre','ciudad','siglas','puntuacion')->get()->sortByDesc("puntuacion")->take(10);
        return $top;
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
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Aeropuerto  $aeropuerto
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {

    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Aeropuerto  $aeropuerto
     * @return \Illuminate\Http\Response
     */
    public function edit(Aeropuerto $aeropuerto)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Aeropuerto  $aeropuerto
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Aeropuerto $aeropuerto)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Aeropuerto  $aeropuerto
     * @return \Illuminate\Http\Response
     */
    public function destroy(Aeropuerto $aeropuerto)
    {
        //
    }
}
