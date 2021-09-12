<?php

namespace App\Http\Controllers;

use App\ReviewAeropuerto;
use App\Aeropuerto;
use App\ReviewAerolinea;
use App\Aerolinea;
use Exception;
use Illuminate\Http\Request;

/**
* @OA\Info(title="Laravel API FutureFlights", version="1.0", description="L5 Swagger Api")
* @OA\Server(url="http://127.0.0.1:8000")
*/

class ReviewController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */

    public function index()
    {

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
     * Display the specified resource.
     *
     * @param  \App\Review  $review
     * @return \Illuminate\Http\Response
     */
    /*
     public function show(Review $review)
    {
        //
    }*/

    /**
     * @OA\Post(
     *      path="/api/aeropuertos/reviews",
     *      summary="Almacenar las reviews de los aeropuertos.",
     *      tags={"Aeropuertos"},
     *      @OA\RequestBody(
     *          description="Reviews de aeropuertos del web scraper.",
     *          required=true,
     *              @OA\JsonContent(
     *                  @OA\Property(property="aeropuerto", type="string"),
     *                  @OA\Property(
     *                      type="array",
     *                      @OA\Items(
     *                              @OA\Property(property="opinion", type="string"),
     *                              @OA\Property(property="compound", type="number"),
     *                      ),
     *                  ),
     *              ),
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Almacena todas las reviews de los aeropuertos.",
     *          @OA\JsonContent(type="object",
     *              @OA\Property(
     *                  @OA\Property(property="opinion", type="string"),
     *                  @OA\Property(property="compound", type="number"),
     *              ),
     *          ),
     *      ),
     *      @OA\Response(response=400, description="Error: Bad Request."),
     *      @OA\Response(response=500, description="Error: Internal Server Error."))
     * )
     */

    public function guardarReviewsAeropuertos(Request $request){

        $lista = array();
        $arrayReviews = $request->json()->all();
        foreach ($arrayReviews as $aeropuerto => $value) {
            $valoracion = 0.0;
            $numeroReviews = 0;
            foreach ($arrayReviews[$aeropuerto] as $opinion => $value2) {

                $review = new ReviewAeropuerto();

                $id = Aeropuerto::select('id')->where('siglas', $aeropuerto)->get();
                $review->id_aeropuerto = $id[0]['id'];
                $review->opinion = $arrayReviews[$aeropuerto][$opinion]['opinion'];
                $review->compound = $arrayReviews[$aeropuerto][$opinion]['compound'];

                if(abs($review->compound)>0.1){
                    array_push($lista, $review->toArray());
                    $valoracion += $review->compound + 1;
                    $numeroReviews++;
                }
                //$review->save();  // Guarda en la base de datos (hace un insert)
            }
            $valoracion = ($valoracion/$numeroReviews)*10/2;
            Aeropuerto::where('siglas', $aeropuerto)->update(array('puntuacion' => $valoracion));
        }
        try{
            ReviewAeropuerto::insert($lista);
            error_log('Reviews Aeropuertos subidas y puntuaciones actualizadas.');
        }
        catch(Exception $e)
        {
           error_log($e->getMessage());
        }
    }

    /**
     * @OA\Post(
     *      path="/api/aerolineas/reviews",
     *      summary="Almacenar las reviews de los aeropuertos.",
     *      tags={"Aerolíneas"},
     *      @OA\RequestBody(
     *          description="Reviews de aerolíneas del web scraper.",
     *          required=true,
     *              @OA\JsonContent(
     *                  type="object",
     *                  @OA\Property(property="aerolínea", type="string"),
     *                  @OA\Property(
     *                      type="array",
     *                      @OA\Items(
     *                          @OA\Property(property="opinion", type="string"),
     *                          @OA\Property(property="compound", type="number"),
     *
     *                      ),
     *
     *                  ),
     *              ),
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Almacena todas las reviews de los aerolíneas.",
     *          @OA\JsonContent(type="object",
     *              @OA\Property(
     *                  @OA\Property(property="opinion", type="string"),
     *                  @OA\Property(property="compound", type="number"),
     *              ),
     *          ),
     *      ),
     *      @OA\Response(response=400, description="Error: Bad Request."),
     *      @OA\Response(response=500, description="Error: Internal Server Error."))
     * )
     */

    public function guardarReviewsAerolineas(Request $request){

        $lista = array();
        $arrayReviews = $request->json()->all();
        foreach ($arrayReviews as $aerolinea => $value) {
            $valoracion = 0.0;
            $numeroReviews = 0;
            foreach ($arrayReviews[$aerolinea] as $opinion => $value2) {

                $review = new ReviewAerolinea();

                $id = Aerolinea::select('id')->where('nombre', $aerolinea)->get();
                $review->id_aerolinea = $id[0]['id'];
                $review->opinion = $arrayReviews[$aerolinea][$opinion]['opinion'];
                $review->compound = $arrayReviews[$aerolinea][$opinion]['compound'];

                if(abs($review->compound)>0.1){
                    array_push($lista, $review->toArray());
                    $valoracion += $review->compound + 1;
                    $numeroReviews++;
                }
                //$review->save();  // Guarda en la base de datos (hace un insert)
            }
            $valoracion = ($valoracion/$numeroReviews)*10/2;
            Aerolinea::where('nombre', $aerolinea)->update(array('puntuacion' => $valoracion));
        }
        ReviewAerolinea::insert($lista);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Review  $review
     * @return \Illuminate\Http\Response
     */

     /*
    public function edit(Review $review)
    {
        //
    }*/

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Review  $review
     * @return \Illuminate\Http\Response
     */
    /*
     public function update(Request $request, Review $review)
    {
        //
    }*/

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Review  $review
     * @return \Illuminate\Http\Response
     */

     /*
    public function destroy(Review $review)
    {
        //
    }*/
}
