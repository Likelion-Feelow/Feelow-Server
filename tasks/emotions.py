class Emotions:
    HAPPY = ['긍정', '행복', '기쁨', '만족', '감사', '희망', '자신감', '흥미', '열정', '자부심', '안심']
    CALM = ['평온', '안정', '편안', '고요', '차분', '여유', '온화', '따뜻함', '수용', '조화', '균형']
    DEPRESSED = ['우울', '슬픔', '절망', '침울', '낙담', '눈물', '후회', '무기력', '고독', '상실', '비관']
    ANXIETY = ['불안', '걱정', '초조', '긴장', '두려움', '공포', '당황', '염려', '불편', '근심', '불확실'] 
    ANGER = ['분노', '화남', '짜증', '격노', '불쾌', '원망', '성남', '분개', '증오', '울분', '분통']
    @staticmethod
    def get_emotion_category(emotion):
        if emotion in Emotions.HAPPY:
            return '긍정'
        elif emotion in Emotions.CALM:
            return '평온'
        elif emotion in Emotions.DEPRESSED:
            return '우울'
        elif emotion in Emotions.ANXIETY:
            return '불안'
        elif emotion in Emotions.ANGER:
            return '분노'
        return None