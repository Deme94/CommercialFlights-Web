<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateReviewsAeropuertosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('reviews_aeropuertos', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            # keys
            $table->integer('id_aeropuerto')->unsigned();
            $table->foreign('id_aeropuerto')->references('id')->on('aeropuertos');
            # campos propios
            $table->longText('opinion')->nullable();
            $table->float('compound');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('reviews_aeropuertos');
    }
}
