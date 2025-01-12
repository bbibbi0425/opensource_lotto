document.addEventListener("DOMContentLoaded", function () {
    // Winning Numbers 필드와 Bonus Number 필드 찾기
    const winningNumbersField = document.getElementById("id_winning_numbers");
    const bonusNumberField = document.getElementById("id_bonus_number");

    // 통계 출력 영역 생성
    const statsContainer = document.createElement("div");
    statsContainer.style.marginTop = "20px";
    statsContainer.style.padding = "10px";
    statsContainer.style.border = "1px solid #ddd";
    statsContainer.style.borderRadius = "10px";
    statsContainer.style.backgroundColor = "#f9f9f9";
    statsContainer.style.fontSize = "14px";
    statsContainer.style.color = "#333";
    statsContainer.style.whiteSpace = "pre-wrap"; // 줄바꿈을 유지

    // 초기 통계 메시지
    statsContainer.textContent = "Loading winner statistics...";

    // 통계 계산 함수
    async function calculateWinnerStatistics() {
        const roundNumber = document.getElementById("id_round_number").value;

        try {
            const response = await fetch(`/?action=check_results&round=${roundNumber}`);
            if (!response.ok) {
                statsContainer.textContent = "Failed to fetch winner statistics.";
                return;
            }

            const data = await response.json();
            const { results, winning_numbers, bonus_number, round } = data;

            const rankCount = results.reduce((acc, ticket) => {
                acc[ticket.rank] = (acc[ticket.rank] || 0) + 1;
                return acc;
            }, {});

            // 통계 출력 텍스트 생성
            let statsText = `🎉 Round ${round}\n`;
            statsText += `Winning Numbers: ${winning_numbers}\n`;
            statsText += `Bonus Number: ${bonus_number}\n\n`;
            statsText += "📊 Winner Statistics:\n";
            Object.entries(rankCount).forEach(([rank, count]) => {
                statsText += ` - ${rank}: ${count}명\n`;
            });

            statsText += "\n📋 Winners:\n";
            results.forEach(ticket => {
                statsText += ` - User: ${ticket.user}, Numbers: ${ticket.numbers}, Rank: ${ticket.rank}\n`;
            });

            // 통계 텍스트를 화면에 출력
            statsContainer.textContent = statsText;
        } catch (error) {
            statsContainer.textContent = "An error occurred while fetching statistics.";
            console.error(error);
        }
    }

    // 페이지 로드 시 통계 계산
    calculateWinnerStatistics();

    // 버튼 생성
    const randomButton = document.createElement("button");
    randomButton.type = "button";
    randomButton.textContent = "Generate Random Numbers";

    // 스타일 추가
    randomButton.style.marginTop = "20px";
    randomButton.style.padding = "10px 20px";
    randomButton.style.borderRadius = "10px";
    randomButton.style.border = "none";
    randomButton.style.backgroundColor = "#007bff";
    randomButton.style.color = "#fff";
    randomButton.style.fontSize = "14px";
    randomButton.style.cursor = "pointer";
    randomButton.style.display = "block";

    // 버튼 클릭 이벤트
    randomButton.addEventListener("click", function () {
        const winningNumbers = Array.from({ length: 6 }, () => Math.floor(Math.random() * 45) + 1);
        const bonusNumber = Math.floor(Math.random() * 45) + 1;

        winningNumbersField.value = winningNumbers.join(",");
        bonusNumberField.value = bonusNumber;

        calculateWinnerStatistics(); // 버튼 클릭 후 통계 업데이트
    });

    // 버튼과 통계 출력 영역을 필드셋의 끝에 추가
    const fieldset = bonusNumberField.closest("fieldset");
    if (fieldset) {
        fieldset.appendChild(randomButton);
        fieldset.appendChild(statsContainer);
    }
});
