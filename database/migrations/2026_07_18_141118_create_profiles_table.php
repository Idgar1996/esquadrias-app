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
        Schema::create('profiles', function (Blueprint $table) {
            $table->id();
            $table->string('code')->unique(); // Ex: SU-001, REQ-025, SU-053
            $table->decimal('weight_per_meter', 6, 3); // Peso técnico por metro linear
            $table->decimal('bar_length', 4, 2)->default(6.00); // Tamanho padrão da barra (geralmente 6 metros)
            $table->string('supplier')->nullable(); // Nome do fabricante/fornecedor
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('profiles');
    }
};
