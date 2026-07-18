<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('margins', function (Blueprint $table) {
            $table->id();
            $table->string('model_name')->unique(); // Ex: Grade, Janela de Correr, Maxim-ar
            $table->decimal('markup_percentage', 5, 2); // Ex: 1.50 (significa 50% de lucro sobre o custo)
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('margins');
    }
};
