<?php

use App\Http\Controllers\AerolineaController;
use App\Http\Controllers\VueloController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/
//login y manejo de usuarios
Route::group([

    'middleware' => 'api',

], function ($router) {

    Route::post('login', 'AuthController@login');
    Route::post('signup', 'AuthController@signup');
    Route::post('logout', 'AuthController@logout');
    Route::post('refresh', 'AuthController@refresh');
    Route::post('me', 'AuthController@me');
    Route::post('sendPasswordResetLink', 'ResetPasswordController@sendEmail');
    Route::post('resetPassword', 'ChangePasswordController@process');

});
// Web scrapers
Route::post('/aeropuertos/reviews', 'ReviewController@guardarReviewsAeropuertos');
Route::post('/clima', 'ClimaController@store');
Route::post('/vuelos', 'VueloController@store');
Route::post('/aerolineas', 'AerolineaController@store');
Route::post('/aerolineas/reviews', 'ReviewController@guardarReviewsAerolineas');
Route::get('/vuelos/recopilar', 'VueloController@recopilar');

// Interfaz
Route::get('/vuelos', 'VueloController@getVuelos');
Route::get('/vuelos/tabla/{id_aeropuerto}', 'VueloController@getVuelos_tabla_id');
Route::get('/aeropuertos', 'AeropuertoController@index');
Route::get('/aeropuertos/nombre', 'AeropuertoController@mostrarNombreAeropuertos');
Route::get('/vuelos/{codigo_vuelo}/{id_aeropuerto}/{fecha}', 'VueloController@getInfoVuelos_espec');
Route::get('/aeropuertos/top', 'AeropuertoController@getTopScore');
Route::get('/aerolineas', 'AerolineaController@index');
Route::get('/aerolineas/top', 'AerolineaController@getTopScore');
Route::get('/aerolineas/{id_aeropuertos}', 'AerolineaController@getAerolineasXpuntuacion');
Route::get('/vuelos/recopilar/estado', 'VueloController@estaRecopilando');
Route::get('/vuelos/recopilar/start', 'VueloController@startRecopilar');
Route::get('/vuelos/recopilar/stop', 'VueloController@stopRecopilar');
Route::get('/clasificador', 'ClasificadorController@getModelo');
Route::get('/clasificador/entrenar', 'ClasificadorController@entrenar');
Route::get('/clasificador/entrenar/estado', 'ClasificadorController@estaEntrenando');
Route::get('/clasificador/entrenar/start', 'ClasificadorController@startEntrenar');
Route::get('/clasificador/entrenar/stop', 'ClasificadorController@stopEntrenar');
Route::get('/aerolineas/retrasos', 'AerolineaController@getRetrasos');
//Route::get('/aerolineas/{id}', 'AerolineaController@show');
//Route::get('/vuelos/{siglas}', 'VueloController@show');
//Route::get('/aeropuertos/retrasos', 'AeropuertoController@getRetrasos');
// Prediccion
Route::get('/vuelos/predecir/{estado}', 'VueloController@getDatosPrediccion');
Route::post('/vuelos/estimaciones', 'VueloController@actualizarEstimaciones');

