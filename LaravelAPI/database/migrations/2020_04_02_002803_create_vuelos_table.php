<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateVuelosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('vuelos', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            # keys
            $table->integer('id_aerolinea')->unsigned();
            $table->integer('id_aeropuerto_salida')->unsigned();
            $table->foreign('id_aerolinea')->references('id')->on('aerolineas');
            $table->foreign('id_aeropuerto_salida')->references('id')->on('aeropuertos');
            # campos propios
            $table->dateTime('date_time');
            $table->text('aeropuerto_destino');
            $table->text('codigo_vuelo');
            $table->text('terminal')->nullable(); # no siempre especifican
            $table->integer('distancia');
            $table->text('hora_programada');
            $table->text('hora_salida')->nullable();
            $table->integer('estado'); #nº entre cancelado, en espera, ya ha salido, etc

        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('vuelos');
    }
}
