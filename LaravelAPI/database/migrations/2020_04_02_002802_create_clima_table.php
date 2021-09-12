<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateClimaTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('clima', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            # keys
            $table->integer('id_aeropuerto')->unsigned();
            $table->foreign('id_aeropuerto')->references('id')->on('aeropuertos');
            # campos propios
            $table->dateTime('date_time');
            $table->text('hora');
            $table->text('cielo');
            $table->integer('temperatura');
            $table->float('lluvia');
            $table->integer('porcentajeLluvia');
            $table->integer('nubes');
            $table->integer('viento');
            $table->integer('rafaga');
            $table->text('direccion_viento')->nullable();
            $table->integer('humedad');
            $table->integer('presion');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('clima');
    }
}
