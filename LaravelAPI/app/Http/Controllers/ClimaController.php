<?php

namespace App\Http\Controllers;

use App\Clima;
use App\Aeropuerto;
use Illuminate\Http\Request;
use Exception;

class ClimaController extends Controller
{
    /**
    * @OA\Post(
    *     path="/api/clima",
    *     summary="Almacenar Clima",
    *     tags={"Clima"},
    *     @OA\RequestBody(
    *           description= "Provide company search parameter",
    *           required= true,
    *           @OA\JsonContent(
    *               type="object",
    *               @OA\Property(property="aeropuerto", type="string"),
    *                * @OA\Property(
        *                  type="array",
        *                  @OA\Items(
                    *               @OA\Property(property="fecha", type="string"),
                    *               @OA\Property(property="hora", type="string"),
                    *               @OA\Property(property="cielo", type="string"),
                    *               @OA\Property(property="temperatura", type="integer"),
                    *               @OA\Property(property="lluvia", type="number"),
                    *               @OA\Property(property="porcentajeLluvia", type="integer"),
                    *               @OA\Property(property="nubes", type="integer"),
                    *               @OA\Property(property="viento", type="integer"),
                    *               @OA\Property(property="rafaga", type="integer"),
                    *               @OA\Property(property="direccion_viento", type="string"),
                    *               @OA\Property(property="humedad", type="integer"),
                    *               @OA\Property(property="presion", type="integer"),
        *                  ),
    *              )
    *           )
    *     ),
    *     @OA\Response(
    *         response=200,
    *         description="Almacena el clima para cada uno de los aeropuertos.",
    *           @OA\JsonContent(
    *               type="array",
        *            @OA\Items(
        *               @OA\Property(property="id", type="integer"),
        *               @OA\Property(property="id_aeropuerto", type="integer"),
        *               @OA\Property(property="date_time", type="string"),
        *               @OA\Property(property="hora", type="string"),
        *               @OA\Property(property="cielo", type="string"),
        *               @OA\Property(property="temperatura", type="integer"),
        *               @OA\Property(property="lluvia", type="number"),
        *               @OA\Property(property="porcentajeLluvia", type="integer"),
        *               @OA\Property(property="nubes", type="integer"),
        *               @OA\Property(property="viento", type="integer"),
        *               @OA\Property(property="rafaga", type="integer"),
        *               @OA\Property(property="direccion_viento", type="string"),
        *               @OA\Property(property="humedad", type="integer"),
        *               @OA\Property(property="presion", type="integer"),
        *                )
    *               )
    *     ),
    *     @OA\Response(response=400, description="Error: Bad Request."),
    *     @OA\Response(response=500, description="Error: Internal Server Error.")
    * )
    */

    public function store(Request $request){

        $lista = array();
        $arrayClimas = $request->json()->all();
        foreach ($arrayClimas as $aeropuerto => $value) {
            foreach ($arrayClimas[$aeropuerto] as $hora => $value2) {

                $clima = new Clima();

                $id = Aeropuerto::select('id')->where('siglas', $aeropuerto)->get();
                $clima->id_aeropuerto = $id[0]['id'];
                $clima->date_time = $arrayClimas[$aeropuerto][$hora]['fecha'];
                $clima->hora = $arrayClimas[$aeropuerto][$hora]['hora'];
                if(count(Clima::select('id')->where('date_time', $clima->date_time)->where('id_aeropuerto', $clima->id_aeropuerto)->where('hora', $clima->hora)->get())!=0){
                    error_log('Error. Ya existe en la BBDD, no es necesario subirlo de nuevo.');
                }
                $clima->cielo = $arrayClimas[$aeropuerto][$hora]['cielo'];
                $clima->temperatura = $arrayClimas[$aeropuerto][$hora]['temperatura'];
                $clima->lluvia = $arrayClimas[$aeropuerto][$hora]['lluvia'];
                $clima->porcentajeLluvia = $arrayClimas[$aeropuerto][$hora]['porcentajeLluvia'];
                $clima->nubes = $arrayClimas[$aeropuerto][$hora]['nubes'];
                $clima->viento = $arrayClimas[$aeropuerto][$hora]['viento'];
                $clima->rafaga = $arrayClimas[$aeropuerto][$hora]['rafaga'];
                $clima->direccion_viento = $arrayClimas[$aeropuerto][$hora]['direccionViento'];
                $clima->humedad = $arrayClimas[$aeropuerto][$hora]['humedad'];
                $clima->presion = $arrayClimas[$aeropuerto][$hora]['presion'];
                array_push($lista, $clima->toArray());
                $clima->save();  // Guarda en la base de datos (hace un insert)
            }
        }
        try{
            //Clima::insert($lista);
            error_log('Climas subidos.');
        }
        catch(Exception $e)
        {
           error_log($e->getMessage());
        }
    }
}
