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
        Schema::create('registrations', function (Blueprint $table) {
            $table->id();
            $table->foreignId('event_id')->constrained()->onDelete('cascade');
            $table->string('user_id')->nullable()->index();
            $table->foreignId('ticket_type_id')->nullable()->constrained()->onDelete('set null');
            $table->string('attendee_name');
            $table->string('attendee_email');
            $table->enum('status', ['pending', 'confirmed', 'cancelled', 'waitlist'])->default('confirmed');
            $table->enum('payment_status', ['pending', 'paid', 'refunded'])->nullable();
            $table->timestamp('checked_in_at')->nullable();
            $table->string('qr_code')->unique()->nullable();
            $table->json('registration_data')->nullable();
            $table->timestamps();
            
            $table->index(['event_id', 'status']);
            $table->index('attendee_email');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('registrations');
    }
};
