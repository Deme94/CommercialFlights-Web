<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateReviewsAerolineasTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('reviews_aerolineas', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            # keys
            $table->integer('id_aerolinea')->unsigned();
            $table->foreign('id_aerolinea')->references('id')->on('aerolineas');
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
        Schema::dropIfExists('reviews_aerolineas');
    }
}
